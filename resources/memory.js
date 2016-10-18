/*global $, _, document */
$(function () {
  'use strict';

  // Die verfügbaren Bilder.
  var imageData = [];

  var $gameBoard = $('#gameBoard');

  // Spielstand
  var guess1 = '';
  var guess2 = '';
  var count = 0;
  var countMatch = 0;
  var century = 0;

  /**
   * Münzdaten (asynchron) laden.
   */
  $.getJSON('data/03-result-memory.json', function (data) {
    imageData = data;
    fillBoard();
  });

  /**
   * Brettgröße aus Auswahl im Menü ermittlen.
   */
  var getNumberOfPairs = function () {
    return parseInt($('.sizeSelection').val(), 10) / 2;
  };

  /**
   * Filterfunktion für Münzdaten aus Auswahl im Menü ermitteln.
   */
  var getCenturyFilter = function () {
      var range = JSON.parse($('.centurySelection').val());
      return function (imageRecord) {
        var year = imageRecord.date;
        return range[0] <= year && year < range[1];
      };
  }

  var createCoinFrontSourcePath = function (coin) {
    var prefix = 'file:///opt/digiverso/kenom_viewer/data/3/media/';
    return prefix + coin.front.replace('_media', '');
  };

  /**
   * Zufällig geordnete Liste von Bildern für die Brettgröße erzeugen.
   */
  var createShuffledImageUrls = function () {
    var numberOfPairs = getNumberOfPairs();
    var filteredCoins = _.filter(imageData, getCenturyFilter());
    var selectedCoins = _.sample(filteredCoins, numberOfPairs);
    var imageUrls = [];
    for (var i = 0; i < numberOfPairs; i++) {
      var coin = selectedCoins[i];
      var imageSize = 300;
      var imageParameters = {
        action: 'image',
        sourcepath: createCoinFrontSourcePath(coin),
        width: 300,
        height: 300,
        rotate: 0,
        resolution: 72,
        thumbnail: true,
        ignoreWatermark: true,
      };
      var imageUrl = 'http://www.kenom.de/content/?' + $.param(imageParameters);

      imageUrls.push(imageUrl);
      imageUrls.push(imageUrl);
    }

    return _.sample(imageUrls, imageUrls.length);
  };

  /**
   * Frisches Spielfeld mit den übergebenen Bildern erzeugen.
   */
  var fillBoard = function () {
    var selectedImageUrls = createShuffledImageUrls();

    // alte Bilder löschen
    $gameBoard.empty();

    // neue Bilder einfügen
    _.each(selectedImageUrls, function (imageUrl) {
      $gameBoard.append('<li><img src="' + imageUrl + '"/></li>');
    });

    // Bild Tags unsichtbar machen
    $gameBoard.find('img').hide();
  };

  var showModal = function () {
    var modal = document.getElementById('myModal');
    modal.style.display = 'block';
    var span = document.getElementsByClassName('close')[0];

    // When the user clicks on <span> (x), close the modal
    $(span).on('click', function () {
      modal.style.display = 'none';
    });

    // $('.modal').show();
    $('.resetButton').show();
  };

  // win
  var win = function () {
    showModal();
  };

  /**
   * Click-Event Handler für die Auswahl von Kacheln.
   */
  $gameBoard.on('click', 'li', function (event) {
    var $Target = $(event.target);
    var $Image = $Target.find('img');

    if ((count < 2) && !$(this).find('img').hasClass('face-up')) {

      // increment guess count, show image, mark it as face up
      count++;
      $Image.show().addClass('face-up');

      //guess #1
      if (count === 1) {
        guess1 = $Image.attr('src');
      }

      //guess #2
      else {
        guess2 = $Image.attr('src');

        // since it's the 2nd guess check for match
        if (guess1 === guess2) {
          console.log('match');
          $gameBoard.find('li img[src="' + guess2 + '"]').addClass('match');
          countMatch++;
        }

        if (countMatch === getNumberOfPairs()) {
          win();
        }

        // else it's a miss
        else {
          console.log('miss');
          setTimeout(function () {
            $gameBoard.find('img:not(.match)')
              .hide()
              .removeClass('face-up');
          }, 1000);
        }

        // reset
        count = 0;
      }
    }
  });

  /**
   * Click Event-Handler für Reset-Knopf.
   */
  $(document).on('click', '.resetButton', function () {
    fillBoard();
    $('#container').show();
    $('.modal').hide();
    countMatch = 0;
  });

  /**
   * Click Event-Handler für das Spielfeld-Größenmenü.
   */
  $(document).on('change', '.sizeSelection, .centurySelection', function () {
    fillBoard();
  });

});
