import Cookies from 'js-cookie';
import $ from 'jquery';

export const PTCGOParser = require('ptcgo-parser');
const XLSX = require('xlsx');

const csrftoken = Cookies.get('csrftoken');
const api_url = '/api';

var workbook;

async function handleFileAsync(e) {
	const file = e.target.files[0];
	const data = await file.arrayBuffer();
	workbook = XLSX.read(data);

	$('#tabular-import-button').removeClass('btn-outline-success');
	makeDropdownOptions( $('#id_sheet_name'), workbook.SheetNames );
	handleSheetChange(e)
	changeTable( workbook.SheetNames[0] );
}

function makeDropdownOptions( $dropdown, options ) {
	$dropdown.empty()
	$.each( options, function( i, option ) {
		$dropdown.append($('<option>', {
			value: option,
			text: option,
		}));
	});
	$dropdown.parent().show()
}

function handleSheetChange(e) {
	const sheetName = $('#id_sheet_name').val();
	const sheetJSON = XLSX.utils.sheet_to_json( workbook.Sheets[sheetName] )
	changeTable( sheetName );
	console.log( sheetJSON[0] );
	makeDropdownOptions( $('#id_cardname_col'), Object.keys(sheetJSON[0]));
	makeDropdownOptions( $('#id_quantity_col'), Object.keys(sheetJSON[0]));
	makeDropdownOptions( $('#id_location_col'), Object.keys(sheetJSON[0]));
	$('#tabular-import-button').prop('disabled', false);
	$('#tabular-import-check-button').prop('disabled', false);
}

function getCardId( row, cardname ) {
	let card_id = PTCGOParser.parseCard(row[cardname])
	if (!card_id) {
		card_id = 'undefined-00'
	}
	if (card_id.includes('undefined')) {
		$('#sjs-A'.concat(row.__rowNum__+1)).parent().addClass('table-danger')
	}
	return card_id
}

function checkChoices( e ) {
	pushBulkChanges( true );
}

function changeTable( sheetName ) {
	$('table').replaceWith($(XLSX.utils.sheet_to_html(workbook.Sheets[sheetName])).addClass('table table-hover'))
}

function uploadData(e) {
	pushBulkChanges();
}

function pushBulkChanges( dry_run = false ) {
	var cardname_col = $('#id_cardname_col').val();
	var quantity_col = $('#id_quantity_col').val();
	var location_col = $('#id_location_col').val();
	var sheet = XLSX.utils.sheet_to_json(workbook.Sheets[$('#id_sheet_name').val()]);
	if (
		(cardname_col === quantity_col) ||
		(cardname_col === location_col) ||
		(location_col === quantity_col)
	) {
		alert('Must select different columns for processing');
		return
	}
	var out_data = sheet.map( (row) => ({
		card_id: getCardId(row, cardname_col),
		quantity: row[quantity_col],
		stash_name: row[location_col]
	}))

	if (dry_run) {
		return
	}

	// Logic for posting to server
	var updateData = {
		update_data: out_data
	};

	// Post
	$.ajax({
		url: api_url+'/import_tabular',
		type: 'POST',
		headers: {'X-CSRFToken': csrftoken},
		data: JSON.stringify(updateData),
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function(resultData){console.log('updated!')},
		failure: function(resultData){console.log('failed')}
	});
}

$(function() {
	$('#id_tabular_file').on("change", handleFileAsync);
	$('#id_tabular_file').removeClass('form-control').addClass('form-control-file');
	$('#id_sheet_name').on("change", handleSheetChange);
	$('#id_sheet_name_group').hide();
	$('#id_cardname_col_group').hide();
	$('#id_quantity_col_group').hide();
	$('#id_location_col_group').hide();
	$('#tabular-import-check-button').on("click", checkChoices);
	$('#tabular-import-button').on("click", uploadData);
});
