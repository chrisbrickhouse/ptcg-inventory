import Cookies from 'js-cookie';
import $ from 'jquery';

export const PTCGOParser = require('ptcgo-parser');

const csrftoken = Cookies.get('csrftoken');
const api_url = '/api';

function getUpdateData( cardEntry ) {
	var card_id = cardEntry.ptcgoio.id
	var qty = cardEntry.amount
	console.log(card_id,qty)
	return {
		'card_id': card_id,
		'quantity': qty
	}
}

function pushBulkChanges( decklistJSON ) {
	var stash_uuid = $('#decklist-textarea').data('stashid')
	var updateData = {
		uuid: stash_uuid,
		update_data: []
	};
	// Process the decklist JSON into updateData
	decklistJSON.cards.forEach( (card) =>
		updateData.update_data.push( getUpdateData( card ) )
	);
	// Post
	$.ajax({
		url: api_url+'/import_decklist',
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
	$('#decklist-import-button').on("click", function() {
		var decklist = $('#decklist-textarea')[0].value;
		var decklistJSON = PTCGOParser.parse(decklist);
		pushBulkChanges( decklistJSON );
	});
});
