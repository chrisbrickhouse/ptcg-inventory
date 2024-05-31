function loadTable( tableId, data ) {
	var rows = '';
	$.each( Object.keys(data), function(index, card_id) {
		function makeInput( name, val, max_n ) {
			var input = '<input class="form-control" style="width: 100%;" type="number" name="';
			input += name;
			input += '" defaultValue="'+val+'" value="'+val+'" ';
			input += 'min="0" max="'+max_n+'" >';
			return input
		};
		var entry = data[card_id];
		var card_name = entry['card_name'];
		var n_from = entry['from_quantity'];
		var n_to = entry['to_quantity'];
		var max_n = parseInt(n_from) + parseInt(n_to);
		var row = '<tr id="'+card_id+'">';
		row += '<td>'+card_id+'</td>';
		row += '<td>'+card_name+'</td>';
		row += '<td>'+makeInput( 'fromQuant', n_from, max_n )+'</td>';
		row += '<td>'+makeInput( 'toQuant', n_to, max_n )+'</td>';
		rows += row + '</tr>';
	});

	function reciprocalInputs( otherName, item ) {
		var defaultVal = parseInt($(item).prop('defaultValue'));
		var diff = parseInt($(item).val()) - defaultVal;
		var $otherQuant = $(item).parent().siblings().find(
			'input[name="'+otherName+'"]'
		);
		$otherQuant.val( $otherQuant.prop('defaultValue') - diff);
	}

	function addReciprocalInput( this_name, other_name ) {
		$('#'+tableId).find(
			'input[name="'+this_name+'"]'
		).each( function( index, item ) {
			$(item).on("change", function() {
				reciprocalInputs( other_name, item );
			});
		});
	}

	$('#' + tableId).find('tbody').html(rows);
	addReciprocalInput( 'fromQuant', 'toQuant' );
	addReciprocalInput( 'toQuant', 'fromQuant' );
	$('#' + tableId).data("table-response", data);
};

function getStashList( fromUUID, toUUID ){
	$.ajax({
		url: api_url+'?action=getBulkMoveTable&from_uuid='+fromUUID+'&to_uuid='+toUUID,
		type: 'GET',
		success: function(response){
			loadTable( 'bulkMoveTable', response )
		}
	});
}

function updateHeader( headerID, $stash ) {
	var stash_name = $stash.find('option:selected').text();
	$('#'+headerID).html('Number in '+stash_name);
}

function pushBulkChanges() {
	var from_stash_uuid = $('#from-stash').val()
	var to_stash_uuid = $('#to-stash').val()
	var $bulkMoveTable = $('#bulkMoveTable')
	var updateData = {
		from_stash: {
			uuid: from_stash_uuid,
			update_data: []
		},
		to_stash: {
			uuid: to_stash_uuid,
			update_data: []
		}
	};
	$bulkMoveTable.find('tbody tr').each(function(index, row) {
		function makeRow( row, name ) {
			function getQuant( name ) {
				return $(row).find('input[name="'+name+'"]').val()
			};
			var card_id = $(row).prop('id')
			updateDataRow = {
				'card_id': card_id,
				'n_card_in_stash': getQuant(name)
			};
			return updateDataRow
		}
		updateData['from_stash']['update_data'].push(makeRow( row, 'fromQuant' ))
		updateData['to_stash']['update_data'].push(makeRow( row, 'toQuant' ))
	});
	$.ajax({
		url: api_url+'/bulkUpdate',
		type: 'POST',
		headers: {'X-CSRFToken': csrf_token},
		data: JSON.stringify(updateData),
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function(resultData){console.log('updated!')},
		failure: function(resultData){console.log('failed')}
	});
}

$(document).ready(function() {
	function updateFromStashHeader() {
		$('#fromHeader').html("Number in "+$fromStash.find('option:selected').text());
	}

	function updateToStashHeader() {
		$('#toHeader').html("Number in "+$toStash.find('option:selected').text());
	}
		
	/*$selectWidgets = $('.filter-select');
	$selectWidgets.select2({
		theme: "bootstrap-5",
		selectionCssClass: "mx-3 mx-md-3",
		dropdownCssClass: "mx-3 mx-md-3",
		//dropdownParent: $selectWidgets.parent()
	});
*/
	$fromStash = $('#from-stash')
	$toStash = $('#to-stash')

	$fromStash.on("change", function() { 
		getStashList($fromStash.val(),$toStash.val());
		updateFromStashHeader();
	});
	$toStash.on("change", function() {
		getStashList($fromStash.val(),$toStash.val());
		updateToStashHeader();
	});
	$('#submitChangesButton').on("click", pushBulkChanges);

	getStashList($fromStash.val(),$toStash.val());
	updateFromStashHeader();
	updateToStashHeader();
})
