// Selecting the song urls and other details
var trackUrl = []; // Define the trackUrl variable outside the event listener
var trackNames= [];  
var albumArtworks=[]; // This is form the player.html while the rest of them are from playerarea.html
var albums= [];
var duration=[];    
document.addEventListener('DOMContentLoaded', function() {
  var songurls = document.querySelectorAll('input[name^="songurl"]');
  var tracknamess= document.querySelectorAll('input[name^="songname"]');
  var artworks= document.querySelectorAll('input[name^="artworks"]');
  var album= document.querySelectorAll('input[name^="albums"]');
  var durations= document.querySelectorAll('input[name^="duration"]');

  durations.forEach(function(element) {
    duration.push(element.value);
  });          
  songurls.forEach(function(element) {
    trackUrl.push(element.value);
  });
  tracknamess.forEach(function(element) {
    trackNames.push(element.value);
  });
  artworks.forEach(function(element) {
    albumArtworks.push(element.value);
  });
  album.forEach(function(element) {
    albums.push(element.value);
  });
});

$(function () {
var volumeSlider = document.getElementById("volume-slider");
  var playerTrack = $("#player-track"),
    bgArtwork = $("#bg-artwork"),
    bgArtworkUrl,
    albumName = $("#album-name"),
    trackName = $("#track-name"),
    albumArt = $("#album-art"),
    sArea = $("#s-area"),
    seekBar = $("#seek-bar"),
    trackTime = $("#track-time"),
    insTime = $("#ins-time"),
    sHover = $("#s-hover"),
    playPauseButton = $("#play-pause-button"),
    playPauseButtonPage = $("#play-pause-button-page"),
    i = playPauseButton.find("i"),
    iPage = playPauseButtonPage.find("i"),
    tProgress = $("#current-time"),
    tTime = $("#track-length"),
    seekT,
    seekLoc,
    seekBarPos,
    cM,
    ctMinutes,
    ctSeconds,
    curMinutes,
    curSeconds,
    durMinutes,
    durSeconds,
    playProgress,
    bTime,
    nTime = 0,
    buffInterval = null,
    tFlag = false,
    playPreviousTrackButton = $("#play-previous"),
    playNextTrackButton = $("#play-next"),
    currIndex = -1;

    $("#equalizer").addClass("hidden");

    var playerTrack = $("#player-track");

    function playPause() {
      setTimeout(function() {
        if (audio.paused) {
          playerTrack.addClass("active");
          albumArt.addClass("active");
          checkBuffering();
          i.attr("class", "fas fa-pause");
          iPage.attr("class", "fas fa-pause");
          audio.play();
          
          // Show the equalizer when music is played
          $("#equalizer").removeClass("hidden");
        } else {
          playerTrack.removeClass("active");
          albumArt.removeClass("active");
          clearInterval(buffInterval);
          albumArt.removeClass("buffering");
          i.attr("class", "fas fa-play");
          iPage.attr("class", "fas fa-play");
          audio.pause();
          
          // Hide the equalizer when music is paused
          $("#equalizer").addClass("hidden");
        }
      }, 300);
    }
    
    var currentSong = document.querySelectorAll(".currentSong");

    currentSong.forEach(function(currentSong) {
      currentSong.addEventListener("click", function(event) {
        event.preventDefault(); // Prevent default link behavior
        var currentsongindex = event.target.dataset.value;
        var songId = event.target.dataset.songid;
        currentsongindex=currentsongindex-1
        console.log("Current index value:", currentsongindex);

        // Send the song ID and song index to the Flask server using AJAX
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/user/song_click", true);
      xhr.setRequestHeader("Content-Type", "application/json");

      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          // Handle the server response if needed
          console.log(xhr.responseText);
        }
      };

      var data = JSON.stringify({ song_id: songId, song_index: currentsongindex });
      xhr.send(data);

        // Setting the current song details
        if (currentsongindex > -1 && currentsongindex < albumArtworks.length) {
          currIndex=currentsongindex;
    
          seekBar.width(0);
          trackTime.removeClass("active");
          tProgress.text("00:00");
          tTime.text("00:00");
    
          currAlbum = albums[currentsongindex];
          currTrackName = trackNames[currentsongindex];
          currArtwork = albumArtworks[currentsongindex];
          currDuration=duration[currentsongindex];
          console.log("track Name : ",currTrackName,"Track duration",currDuration)
          tTime.text(currDuration);
          audio.src = trackUrl[currentsongindex];
    
          nTime = 0;
          bTime = new Date();
          bTime = bTime.getTime();
    
          albumName.text(currAlbum);
          trackName.text(currTrackName);
          tTime.text(currDuration);
          albumArt.find("img.active").removeClass("active");
          $("#" + currArtwork).addClass("active");
    
          bgArtworkUrl = $("#" + currArtwork).attr("src");
    
          bgArtwork.css({ "background-image": "url(" + bgArtworkUrl + ")" });
        }
        // Audio play logic
        setTimeout(function() {
          if (audio.paused) {
            playerTrack.addClass("active");
            albumArt.addClass("active");
            checkBuffering();
            i.attr("class", "fas fa-pause");
            iPage.attr("class", "fas fa-pause");
            audio.play();
            
            // Show the equalizer when music is played
            $("#equalizer").removeClass("hidden");
          }
        }, 300);
      });
    });

  function showHover(event) {
    seekBarPos = sArea.offset();
    seekT = event.clientX - seekBarPos.left;
    seekLoc = audio.duration * (seekT / sArea.outerWidth());

    sHover.width(seekT);

    cM = seekLoc / 60;

    ctMinutes = Math.floor(cM);
    ctSeconds = Math.floor(seekLoc - ctMinutes * 60);

    if (ctMinutes < 0 || ctSeconds < 0) return;

    if (ctMinutes < 0 || ctSeconds < 0) return;

    if (ctMinutes < 10) ctMinutes = "0" + ctMinutes;
    if (ctSeconds < 10) ctSeconds = "0" + ctSeconds;

    if (isNaN(ctMinutes) || isNaN(ctSeconds)) insTime.text("--:--");
    else insTime.text(ctMinutes + ":" + ctSeconds);

    insTime.css({ left: seekT, "margin-left": "-21px" }).fadeIn(0);
  }

  function hideHover() {
    sHover.width(0);
    insTime.text("00:00").css({ left: "0px", "margin-left": "0px" }).fadeOut(0);
  }

  function playFromClickedPos() {
    audio.currentTime = seekLoc;
    seekBar.width(seekT);
    hideHover();
  }

  function updateCurrTime() {
    nTime = new Date();
    nTime = nTime.getTime();

    if (!tFlag) {
      tFlag = true;
      trackTime.addClass("active");
    }

    curMinutes = Math.floor(audio.currentTime / 60);
    curSeconds = Math.floor(audio.currentTime - curMinutes * 60);

    durMinutes = Math.floor(audio.duration / 60);
    durSeconds = Math.floor(audio.duration - durMinutes * 60);

    playProgress = (audio.currentTime / audio.duration) * 100;

    if (curMinutes < 10) curMinutes = "0" + curMinutes;
    if (curSeconds < 10) curSeconds = "0" + curSeconds;

    if (durMinutes < 10) durMinutes = "0" + durMinutes;
    if (durSeconds < 10) durSeconds = "0" + durSeconds;

    if (isNaN(curMinutes) || isNaN(curSeconds)) tProgress.text("00:00");
    else tProgress.text(curMinutes + ":" + curSeconds);

    if (isNaN(durMinutes) || isNaN(durSeconds)) tTime.text("00:00");
    else tTime.text(currDuration);

    if (
      isNaN(curMinutes) ||
      isNaN(curSeconds) ||
      isNaN(durMinutes) ||
      isNaN(durSeconds)
    )
      trackTime.removeClass("active");
    else trackTime.addClass("active");

    seekBar.width(playProgress + "%");

    if (playProgress == 100) {
      i.attr("class", "fa fa-play");
      iPage.attr("class", "fas fa-play");
      seekBar.width(0);
      tProgress.text("00:00");
      albumArt.removeClass("buffering").removeClass("active");
      clearInterval(buffInterval);
      $("#equalizer").addClass("hidden");
    }
  }

  function checkBuffering() {
    clearInterval(buffInterval);
    buffInterval = setInterval(function () {
      if (nTime == 0 || bTime - nTime > 1000) albumArt.addClass("buffering");
      else albumArt.removeClass("buffering");

      bTime = new Date();
      bTime = bTime.getTime();
    }, 100);
  }

  function selectTrack(flag) {
    console.log("currIndex value:", currIndex);
    if (flag == 0 || flag == 1) ++currIndex;
    else --currIndex;

    if (currIndex > -1 && currIndex < albumArtworks.length) {
      if (flag == 0) 
      {
        i.attr("class", "fa fa-play");
        iPage.attr("class", "fas fa-play");
      }
      else {
        albumArt.removeClass("buffering");
        i.attr("class", "fa fa-pause");
        iPage.attr("class", "fas fa-pause");
      }

      seekBar.width(0);
      trackTime.removeClass("active");
      tProgress.text("00:00");
      tTime.text("00:00");

      currAlbum = albums[currIndex];
      currTrackName = trackNames[currIndex];
      currArtwork = albumArtworks[currIndex];
      currDuration=duration[currIndex];
      audio.src = trackUrl[currIndex];

      nTime = 0;
      bTime = new Date();
      bTime = bTime.getTime();

      if (flag != 0) {
        audio.play();
        playerTrack.addClass("active");
        albumArt.addClass("active");

        clearInterval(buffInterval);
        checkBuffering();
      }

      albumName.text(currAlbum);
      trackName.text(currTrackName);
      tTime.text(currDuration);
      albumArt.find("img.active").removeClass("active");
      $("#" + currArtwork).addClass("active");

      bgArtworkUrl = $("#" + currArtwork).attr("src");

      bgArtwork.css({ "background-image": "url(" + bgArtworkUrl + ")" });
    } else {
      if (flag == 0 || flag == 1) --currIndex;
      else ++currIndex;
    }
  }
  
  var muteButton = document.getElementById("volume-control");
  var volumeSlider = document.getElementById("volume-slider");
  var previousVolume = 1; // Store the previous volume value
  var previousslider = 1; // Store the previous slider value
  
  
  muteButton.addEventListener("click", function() {
    if (audio.volume === 0) {
      // Unmute the audio
      audio.volume = previousVolume;
      volumeSlider.value = previousVolume;
      muteButton.querySelector("i").classList.remove("fa-volume-off");
      muteButton.querySelector("i").classList.add("fa-volume-up");
    } else {
      // Mute the audio
      previousVolume = audio.volume;
      audio.volume = 0;
      volumeSlider.value = 0;
      muteButton.querySelector("i").classList.remove("fa-volume-up");
      muteButton.querySelector("i").classList.add("fa-volume-off");
    }
  });
volumeSlider.addEventListener("change", function() {
  var min = parseFloat(volumeSlider.min);
  var max = parseFloat(volumeSlider.max);
  var value = parseFloat(volumeSlider.value);

  var volume = (value - min) / (max - min);
  audio.volume = volume;
});
volumeSlider.addEventListener("input", function() {
  var sliderValue = volumeSlider.value;
  audio.volume = sliderValue / 100;
  
  if (sliderValue == 0) {
    // Set the mute icon when slider value is 0
    muteButton.querySelector("i").classList.remove("fa-volume-up");
    muteButton.querySelector("i").classList.add("fa-volume-off");
  } else {
    muteButton.querySelector("i").classList.remove("fa-volume-off");
    muteButton.querySelector("i").classList.add("fa-volume-up");
  }
});

  function initPlayer() {
    audio = new Audio();

    selectTrack(0);

    audio.loop = false;

    playPauseButton.on("click", playPause);
    playPauseButtonPage.on("click", playPause);

    sArea.mousemove(function (event) {
      showHover(event);
    });

    sArea.mouseout(hideHover);

    sArea.on("click", playFromClickedPos);

    $(audio).on("timeupdate", updateCurrTime);

    playPreviousTrackButton.on("click", function () {
      selectTrack(-1);
    });
    playNextTrackButton.on("click", function () {
      selectTrack(1);
    });

    $(audio).on("ended", function() {
      selectTrack(1);
    });

  }

  initPlayer();
  
});


// Add the following code inside the playPause() function

var waveContainer = document.getElementById("wave-container");
var wavePatternCanvas = document.getElementById("wave-pattern");
var wavePatternCtx = wavePatternCanvas.getContext("2d");
var waveAmplitude = 10; // Adjust the wave amplitude as desired
var waveSpeed = 0.05; // Adjust the wave speed as desired

function setCanvasSize() {
  wavePatternCanvas.width = waveContainer.clientWidth;
  wavePatternCanvas.height = waveContainer.clientHeight;
}

function drawWavePattern() {
  var waveformHeight = wavePatternCanvas.height / 2;
  var waveformWidth = wavePatternCanvas.width;
  var currentTime = audio.currentTime;
  wavePatternCtx.clearRect(0, 0, waveformWidth, waveformHeight * 2);
  
  wavePatternCtx.beginPath();
  wavePatternCtx.moveTo(0, waveformHeight);
  
  for (var x = 0; x < waveformWidth; x++) {
    var y = Math.sin((currentTime + x * waveSpeed) * 2 * Math.PI) * waveAmplitude + waveformHeight;
    wavePatternCtx.lineTo(x, y);
  }
  
  wavePatternCtx.strokeStyle = "#fd6d94"; // Adjust the wave color as desired
  wavePatternCtx.lineWidth = 2; // Adjust the wave line width as desired
  wavePatternCtx.stroke();
  
  requestAnimationFrame(drawWavePattern);
}

// Call the setCanvasSize() function when the page loads and on window resize
window.addEventListener("load", setCanvasSize);
window.addEventListener("resize", setCanvasSize);

// Call the drawWavePattern function when the song is played
audio.addEventListener("play", function () {
  drawWavePattern();
});

// Call the cancelAnimationFrame function when the song is paused
audio.addEventListener("pause", function () {
  cancelAnimationFrame(drawWavePattern);
});

function pause() {
  $('#equalizer').toggleClass('paused');
}



