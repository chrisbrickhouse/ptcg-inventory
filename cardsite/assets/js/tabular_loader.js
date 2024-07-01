import Cookies from 'js-cookie';
import $ from 'jquery';

export const PTCGOParser = require('ptcgo-parser');
const XLSX = require('xlsx');

const csrftoken = Cookies.get('csrftoken');
const api_url = '/api';

var workbook;
var error = false;

// Plugin from https://stackoverflow.com/posts/8584217/revisions
// Adds attr.changeElementType
(function($) {
    $.fn.changeElementType = function(newType) {
        var attrs = {};

        $.each(this[0].attributes, function(idx, attr) {
            attrs[attr.nodeName] = attr.nodeValue;
        });

        this.replaceWith(function() {
            return $("<" + newType + "/>", attrs).append($(this).contents());
        });
    };
})($);

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
		error = true
	}
	if (card_id.includes('undefined')) {
		$('#sjs-A'.concat(row.__rowNum__+1)).parent().addClass('table-danger')
		error = true
	}
	console.log(error)
	return card_id
}

function checkChoices( e ) {
	if (pushBulkChanges( true )) {
		$('#tabular-import-check-button').removeClass('btn-primary').addClass('btn-danger').text('Check failed')
		$('#tabular-import-button').prop('disabled',true)
	} else {
		$('#tabular-import-check-button').removeClass('btn-primary btn-danger').addClass('btn-success').text('Check passed').prop('disabled',true)
		$('#tabular-import-button').prop('disabled', false).removeClass('btn-secondary').addClass('btn-primary')
	}
}

function changeTable( sheetName ) {
	$('table').replaceWith($(XLSX.utils.sheet_to_html(workbook.Sheets[sheetName])).addClass('table table-hover'))
	$('table').prepend('<thead class="thead-light"></thead>')
	$('tbody').find('>:first-child').prependTo('table thead')
	$('thead td').changeElementType('th')
}

function uploadData(e) {
	pushBulkChanges();
}

function pushBulkChanges( dry_run = false ) {
	var cardname_col = $('#id_cardname_col').val();
	var quantity_col = $('#id_quantity_col').val();
	var location_col = $('#id_location_col').val();
	var sheet = XLSX.utils.sheet_to_json(workbook.Sheets[$('#id_sheet_name').val()]);
	// Reset error latch
	error = false;
	if (
		(cardname_col === quantity_col) ||
		(cardname_col === location_col) ||
		(location_col === quantity_col)
	) {
		alert('Must select different columns for processing');
		error = true
		return error
	}
	var out_data = sheet.map( (row) => ({
		card_id: getCardId(row, cardname_col),
		quantity: row[quantity_col],
		stash_name: row[location_col]
	}))

	if (dry_run) {
		return error
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
