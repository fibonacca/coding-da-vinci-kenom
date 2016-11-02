/*global $, _, document, window */
$(function () {
    'use strict';

    // Die verfügbaren Bilder.
    var imageData = [];

    var $gameBoard = $('#gameBoard');

    // CSS-Klassen
    var foundClass = 'found';
    var peekClass = 'peek';
    var timeoutClass = 'timeout';
    var lastSelectionClass = 'lastSelection';
    var selectionInfoClass = 'selectionInfo';

    // Namen für Datenfelder and DOM-Elementen
    var identifierDataName = 'identifier';
    var descriptionDataName = 'description';
    var moveCountDataName = 'moveCount';
    var startTimeDataName = 'startTime';
    var timerIdDataName = 'timerId';

    /**
     * Die Anzahl der Memory-Karten auf dem Spielfeld.
     */
    var getBoardDimensions = function () {
        return JSON.parse($('.sizeSelection').val());
    };

    /**
     * Brettgröße aus Auswahl im Menü ermittlen.
     */
    var getNumberOfPairs = function (boardDimensions) {
        return boardDimensions[0] * boardDimensions[1] / 2;
    };

    /**
     * Filterfunktion für Münzdaten aus Auswahl im Menü ermitteln.
     */
    var getCenturyFilter = function () {
        var range = JSON.parse($('.centurySelection').val());
        return function (imageRecord) {
            var year = imageRecord.year;
            return range[0] <= year && year < range[1];
        };
    };

    /**
     * Ist der schwierige Spielmodus, bei dem die Vorder- und
     * Rückseite derselben Münze zusammengefunden werden müssen,
     * aktiviert?
     */
    var isDifficult = function () {
        return $('.difficult').prop('checked');
    };

    /**
     * Pfad-URL zum Bild für die Münze.
     * useBack: false/true -> Vorderseite/Rückseite
     */
    var createCoinSourcePath = function (coin, useBack) {
        var prefix = 'file:///opt/digiverso/kenom_viewer/data/' + coin.magic + '/media/';
        var folderName = 'record_' + coin.id;
        var sideSuffix = useBack ? '_rs' : '_vs';
        var fileName = folderName + sideSuffix + '.jpg';
        return prefix + folderName + '/' + fileName;
    };

    /**
     * Erzeugt die vollständige Bild-URL für die gegebene
     * Münze und Seite.
     */
    var createImageUrl = function (coin, useBack) {
        var imageSize = 300;
        var imageParameters = {
            action: 'image',
            sourcepath: createCoinSourcePath(coin, useBack),
            width: imageSize,
            height: imageSize,
            rotate: 0,
            resolution: 72,
            thumbnail: true,
            ignoreWatermark: true
        };
        return 'http://www.kenom.de/content/?' + $.param(imageParameters);
    };

    /**
     * Zufällig geordnete Liste von Bildern für die Brettgröße erzeugen.
     */
    var shuffleCoins = function (boardDimensions) {
        var numberOfPairs = getNumberOfPairs(boardDimensions);
        var filteredCoins = _.filter(imageData, getCenturyFilter());
        var selectedCoins = _.sample(filteredCoins, numberOfPairs);
        var shuffled = _.flatten(
            _.map(selectedCoins, function (coin) {
                var firstCopy = _.clone(coin);
                firstCopy.back = false;
                var secondCopy = _.clone(coin);
                secondCopy.back = isDifficult();
                return [firstCopy, secondCopy];
            })
        );

        return _.sample(shuffled, shuffled.length);
    };

    var setBoardSize = function ($board, boardDimensions) {
        $board.removeClass();

        var w = window.innerWidth;
        var h = window.innerHeight - 50;
        var ratio = w / h;

        var columnCount = ratio > 1 ? boardDimensions[0] : boardDimensions[1];

        $board.addClass('columns-' + columnCount);
        $board.css({
            width: w - 25
        });
    };

    /**
     * Frisches Spielfeld mit den übergebenen Bildern erzeugen.
     */
    var fillBoard = function () {
        var boardDimensions = getBoardDimensions();
        var shuffledCoins = shuffleCoins(boardDimensions);

        // alte Bilder löschen
        $gameBoard.empty();
        setBoardSize($gameBoard, boardDimensions);

        // neue Bilder einfügen
        _.each(shuffledCoins, function (coin) {
            var li = document.createElement('li');
            var imageUrl = createImageUrl(coin, coin.back);
            var identifyingString = imageUrl.replace(/.*record_/, '').replace(/_[vr]s.*/, '');
            li.setAttribute('data-' + identifierDataName, identifyingString);
            li.setAttribute('data-' + descriptionDataName, coin.title);
            li.setAttribute('class', 'cell');

            var img = document.createElement('img');
            img.setAttribute('src', imageUrl);
            img.setAttribute('alt', 'Spielstein');
            li.appendChild(img);

            $gameBoard.append(li);
        });
    };

    var showModal = function () {
        var modal = document.getElementById('myModal');
        modal.style.display = 'block';

        // When the user clicks on <span> (x), close the modal
        $('.close', modal).on('click', function () {
            modal.style.display = 'none';
        });

        var clicks = $gameBoard.data(moveCountDataName);
        var duration = Math.floor(
            (Date.now() - $('.timer').data(startTimeDataName))
            / 1000
        );
        var infoText = clicks + ' Klicks in ' + duration + ' Sekunden';
        $('.modal-footer .details').text(infoText);

        $('.resetButton').show();
    };

    var clearTimer = function () {
        clearInterval($gameBoard.data(timerIdDataName));
        $('.timer').empty();
    };

    // win
    var win = function () {
        clearTimer();
        showModal();
    };

    var updateClickCount = function (newCount) {
        $gameBoard.data(moveCountDataName, newCount);
        var jMoves = $('.moves');
        if (newCount === 0) {
            jMoves.text('');
        } else if (newCount === 1) {
            jMoves.text(' 1 Klick');
        } else {
            jMoves.text(newCount + ' Klicks');
        }

        // Beim ersten Klick den Timer starten.
        if (newCount === 1) {
            var startTime = Date.now();
            var jTimer = $('.timer');
            jTimer.data(startTimeDataName, startTime);
            var timerId = setInterval(function () {
                var duration = Math.floor((Date.now() - startTime) / 1000);
                jTimer.text(duration + 's');
            }, 1000);
            $gameBoard.data(timerIdDataName, timerId);
        }
    };

    var updateLastSelectionText = function () {
        var $lastSelected = $('.' + lastSelectionClass);
        var newText = $lastSelected.length > 0
            ? $lastSelected.data(descriptionDataName)
            : '';
        $('.' + selectionInfoClass).text(newText);
    };

    var setLastSelection = function ($element) {
        $('.' + lastSelectionClass).removeClass(lastSelectionClass);
        $element.addClass(lastSelectionClass);
        updateLastSelectionText();
    };

    var removePeek = function ($elements) {
        $elements
            .removeClass(peekClass)
            .removeClass(timeoutClass)
            .removeClass(lastSelectionClass)
            .removeAttr('title');
        updateLastSelectionText();
    };

    /**
     * Click-Event Handler für die Auswahl von Kacheln.
     */
    $gameBoard.on('click', 'li', function (event) {
        var $target = $(event.currentTarget);

        // Klicks auf bereits gefundene oder umgedrehte Karte ignorieren.
        if ($target.hasClass(foundClass) || $target.hasClass(peekClass)) {
            return;
        }

        updateClickCount($gameBoard.data(moveCountDataName) + 1);

        // War vorher mehr als eine Karte aufgedeckt, aufgedeckte Karten zurückdrehen.
        var $oldPeek = $gameBoard.find('.' + peekClass);
        if ($oldPeek.length > 1) {
            removePeek($oldPeek);
        }

        // Geklickte Karte aufdecken.
        $target
            .addClass(peekClass)
            .attr('title', $target.data(descriptionDataName));

        setLastSelection($target);

        // Nach dem Aufdecken aufgedeckte Karten vergleichen und zum Zurückdrehen markieren, bzw fixieren.
        var $newPeek = $gameBoard.find('.' + peekClass);
        if ($newPeek.length === 2) {
            if ($newPeek.first().data(identifierDataName) === $newPeek.last().data(identifierDataName)) {
                $newPeek
                    .addClass(foundClass)
                    .removeClass(peekClass);
            } else {
                $newPeek.addClass(timeoutClass);
                setTimeout(function () {
                    removePeek(
                        $newPeek.filter(function (index, element) {
                            return $(element).hasClass(timeoutClass);
                        })
                    );
                }, 2000);
            }
        }

        if ($gameBoard.find('.cell:not(.found)').length === 0) {
            win();
        }
    });

    /**
     * Brett neu aufbauen und Spielstand zurücksetzen.
     */
    var resetGame = function () {
        fillBoard();
        $('#container').show();
        $('.modal').hide();
        updateClickCount(0);
        clearTimer();
    };

    /**
     * Event-Handler zum Neustart des Spiels
     */
    $(document)
    // für Knöpfe und Checkbox
        .on('click', '.resetButton, .restartGame, .difficult', resetGame)
    // für Änderungen der Menüauswahl
        .on('change', '.sizeSelection, .centurySelection', resetGame);

    /**
     * Münzdaten (asynchron) laden.
     */
    $.getJSON('https://raw.githubusercontent.com/ssp/coding-da-vinci-kenom/master/analyse/06-result-memory.json', function (data) {
        imageData = data;
        resetGame();
    });

});
