export const PTCGOParser = require('ptcgo-parser');

$(function() {
	$('#decklist-import-button').on("click", function() {
		var decklist = $('#decklist-textarea')[0].value;
		console.log(decklist);
		console.log(PTCGOParser.parse(decklist))
	});
});
