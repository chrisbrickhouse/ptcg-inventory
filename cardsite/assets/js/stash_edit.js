import Cookies from "js-cookie";
import $ from "jquery";
import "select2";
import "select2/dist/css/select2.css";
import "select2-bootstrap-5-theme/dist/select2-bootstrap-5-theme.min.css";

const csrftoken = Cookies.get("csrftoken");
const api_url = "/api";
var stash_uuid;
var post_url;

$(function () {
  function fetchCardCount(card_id) {
    var ajaxQuery = {
      url:
        api_url +
        "?action=countDeckCard&card_id=" +
        card_id +
        "&deck_uuid=" +
        stash_uuid,
      type: "get",
      success: function (response) {
        $("#card-count-display").val(response);
      },
      failure: function (response) {
        console.log(response);
      },
    };
    $.ajax(ajaxQuery);
  }

  function incrementCardCount(step) {
    var $cardCountDisplay = $("#card-count-display");
    var displayValue = $cardCountDisplay.val();
    if (displayValue) {
      if (displayValue < 1 && step < 0) {
        return;
      }
      $cardCountDisplay.val(parseInt($cardCountDisplay.val()) + step);
    } else {
      $cardCountDisplay.val(0);
      incrementCardCount(step);
    }
  }

  function resetCardCount() {
    fetchCardCount($(".filter-select").val());
  }

  function postDeckChange() {
    var card_id = $(".filter-select").val();
    var quantity = $("#card-count-display").val() | 0;
    var post_data = {
      card_id: card_id,
      quantity: quantity,
      csrfmiddlewaretoken: csrftoken,
    };
    $.ajax({
      url: post_url,
      type: "POST",
      data: post_data,
      success: function (resultData) {
        console.log(resultData);
      },
      failute: function (resultData) {
        console.log(resultData);
      },
    });
  }

  //function updateDeckTable() {
  //  var $deckTableBody = $("#deckListTable > tbody");
  //}

  post_url = $("#data-span").data("post-url");
  stash_uuid = $("#data-span").data("stash-uuid");

  var $cardSelect = $(".filter-select");

  console.log($cardSelect.width());
  $cardSelect.select2({
    theme: "bootstrap-5",
    selectionCssClass: "mx-3 mx-md-0",
    dropdownCssClass: "mx-3 mx-md-0",
    dropdownParent: $cardSelect.parent(),
  });
  $cardSelect.on("select2:selecting", function () {
    postDeckChange();
  });
  $cardSelect.on("select2:open", function () {
    console.log("here");
    $(".select2-dropdown").width($(".select2").width() - 2);
  });
  $cardSelect.on("change", function () {
    resetCardCount();
  });
  $("#card-count-increase").click(function () {
    incrementCardCount(1);
  });
  $("#card-count-decrease").click(function () {
    incrementCardCount(-1);
  });

  resetCardCount();
});
