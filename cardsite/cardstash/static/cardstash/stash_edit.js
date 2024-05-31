$(document).ready(function() {
	function fetchCardCount( card_id ) {
		var ajaxQuery = {
			url: api_url+"?action=countDeckCard&card_id="+card_id+"&deck_uuid="+stash_uuid,
			type: 'get',
			success: function( response ) {
				$('#card-count-display').val( response );
			},
			failure: function( response ) {
				console.log(response);
			}
		};
		$.ajax(ajaxQuery)
	}

	function incrementCardCount( step ) {
	  $cardCountDisplay = $('#card-count-display')
		displayValue = $cardCountDisplay.val()
	  if (displayValue) {
	    if ((displayValue < 1) && (step < 0)) {
		return;
	    }
	    $cardCountDisplay.val( parseInt($cardCountDisplay.val()) + step )
	  } else {
	    $cardCountDisplay.val( 0 )
	    incrementCardCount( step )
	  }
	}

	function resetCardCount() {
		fetchCardCount( $('.filter-select').val() );
	}

	function postDeckChange() {
		card_id = $('.filter-select').val();
		quantity = $('#card-count-display').val() | 0;
		post_data = {
			card_id: card_id,
			quantity: quantity,
			csrfmiddlewaretoken: csrf_token
		};
		$.ajax({
			url: post_url,
			type: 'POST',
			data: post_data,
			success: function(resultData) { console.log(resultData) },
			failute: function(resultData) { console.log(resultData) }
		});
	}

	function updateDeckTable() {
		$deckTableBody = $('#deckListTable > tbody')
	}


	$cardSelect = $('.filter-select');

	$cardSelect.select2();
	$cardSelect.on("select2:selecting", function(){ postDeckChange(); });
	$cardSelect.on("change", function(){ resetCardCount(); });
	$('#card-count-increase').click(function(){incrementCardCount(1)});
	$('#card-count-decrease').click(function(){incrementCardCount(-1)});

	resetCardCount();
});
