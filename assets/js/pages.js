/**
    The logic to work with mobile menu.
*/
var menuElement = document.getElementById("id-mobile-menu");
var menuClass = "show";
function showMenu() {
    arr = menuElement.className.split(" ");
    if (arr.indexOf(menuClass) == -1) {
        menuElement.className += " " + menuClass;
    }
}
function hideMenu() {
    menuElement.className = menuElement.className.replace(/\bshow\b/g, "");
}

function bottomFixedBlockPosition(scrolled) {

    var bottomFixedElement = document.getElementById("id-bottom-block-fixed");

    if (bottomFixedElement) {
        var footerHeight = document.getElementsByClassName('footer')[0].clientHeight;
        var documentHeight = document.body.clientHeight;
        var windowHeight = document.documentElement.clientHeight;
        var breakHeight = documentHeight - windowHeight - footerHeight;

        var bottomElementClasses = bottomFixedElement.className.split(" ");
        var relativeClass = 'relative';

        if (scrolled > breakHeight) {
            if (bottomElementClasses.indexOf(relativeClass) === -1) {
                bottomFixedElement.className += ' ' + relativeClass;
            }
        } else {
            if (bottomFixedElement.className.split(' ').length > 1) {
                bottomFixedElement.className = "bottom-block-fixed";
            }
        }
    }
}

/**
 * The logic must be applied when user scroll.
*/
window.onscroll = function() {
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    /** Work with bottom fixed block */
    bottomFixedBlockPosition(scrolled);
}

/**
 * The logic to align block height.
*/
function alignHeighElements(wrapperElement, targetElement) {
    var wrappers = document.getElementsByClassName(wrapperElement);
    for (var i=0; i<wrappers.length; i++) {
        var blockHeights = [];

        var childrens = wrappers[i].getElementsByClassName(targetElement);

        for (var n=0; n<childrens.length; n++) {
            childrens[n].style.height = 'auto';
        }

        for (var n=0; n<childrens.length; n++) {
            blockHeights.push(childrens[n].clientHeight);
        }

        var maxHeight = Math.max.apply(Math, blockHeights);
        for (var n=0; n<childrens.length; n++) {
            childrens[n].style.height = maxHeight + 'px';
        }

    }
}

/**
 * Makes the height for the element as for given one.
*/
function makeHeightTheSame(sourceElem, targetElem) {
    if (document.getElementById(sourceElem)) {
        document.getElementById(targetElem).style.height = document.getElementById(sourceElem).clientHeight + 'px';
    }
}


function alignAllHeights() {
    alignHeighElements('organize-items', 'item');
    alignHeighElements('advanced-experience', 'expr');
    alignHeighElements('recent-items', 'two-columns');
    alignHeighElements('key-facts', 'fact');
    alignHeighElements('project-to-product', 'content');
    alignHeighElements('blog-content', 'info');
    alignHeighElements('facts', 'fact');
    alignHeighElements('circle-container', 'circle-block');
    makeHeightTheSame('id-bottom-block-fixed', 'id-bottom-fixed-block-area');
}

alignAllHeights();

/**
 * Resize browser event.
*/
window.onresize = function(event) {
    setTimeout(function() {
        alignAllHeights();
    }, 1000);
};


var linkButtons = document.getElementsByClassName('js-block-link');
for (let i=0; i<linkButtons.length; i++) {
    if (linkButtons[i].getAttribute('data-link') !== 'None') {
        linkButtons[i].onclick = function() {
            window.location.href = linkButtons[i].getAttribute('data-link');
        }
    }
}

/**
 * Contact us form.
*/
  // using jQuery
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $(document).ready(function() {
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
  });

var frm = $('#contact_form');
frm.submit(function (e) {
    e.preventDefault();
    $.each($("div[class^='contact_form_']"), function(ind, value){
        $(value).hide();
        $(value).prev().css('border', 'none')
    })
    var formData = new FormData($('#contact_form')[0]);

    // Attach file
    var ajax = new XMLHttpRequest();
    ajax.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                if (JSON.parse(ajax.responseText).result == 'error') {
                    $.each(JSON.parse(ajax.responseText).response, function(key, value) {
                        $('.contact_form_' + key).css('display', 'block')
                        $('.contact_form_' + key).prev().css("border", '1px solid #FD7900')
                        $('.contact_form_' + key).text(value)
                    })
                } else {
                    location.reload();
                }
            }
    }
    ajax.open("POST", '');
    ajax.send(formData);
});

//Map
$('.usa-pin').mouseenter(function() {
    $('.usa').show();
    $('.little_union').show();
    $('.usa-address').show();
    $('.main_map').hide()
}).mouseleave(function(){
    $('.usa').hide();
    $('.little_union').hide();
    $('.usa-address').hide();
    $('.main_map').show()
});

$('.england-pin').mouseenter(function() {
    $('.england').show();
    $('.big_union').show();
    $('.england-address').show();
    $('.main_map').hide()
}).mouseleave(function(){
    $('.england').hide();
    $('.big_union').hide();
    $('.england-address').hide();
    $('.main_map').show()
});

$('.ukraine-pin').mouseenter(function() {
    $('.ukraine').show();
    $('.little_union').show();
    $('.ukraine-address').show();
    $('.main_map').hide()
}).mouseleave(function(){
    $('.ukraine').hide();
    $('.little_union').hide();
    $('.ukraine-address').hide();
    $('.main_map').show()
});


//File upload progressbar
function _(el) {
  return document.getElementById(el);
}

function uploadFile() {
  var file = $('#id_file')[0].files[0];
  $('.progressbar').css('display', 'block')
  $('.file_name').text(file.name)
  $('.file_size').text((file.size/1000).toFixed(1) + 'Kb');
  var url = $('#progressBar').data('url')
  var formdata = new FormData();
  formdata.append("file1", file);
  formdata.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"').val());
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", progressHandler, false);
  ajax.addEventListener("load", completeHandler, false);
  ajax.addEventListener("error", errorHandler, false);
  ajax.addEventListener("abort", abortHandler, false);
  ajax.open("POST", url);
  ajax.send(formdata);
}

function progressHandler(event) {
  _("loaded_n_total").innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
  var percent = (event.loaded / event.total) * 100;
  _("progressBar").value = Math.round(percent);
  _("status").innerHTML = Math.round(percent) + "% uploaded... please wait";
}

function completeHandler(event) {
  _("status").innerHTML = event.target.responseText;
  _("progressBar").value = 0; //wil clear progress bar after successful upload
}

function errorHandler(event) {
  _("status").innerHTML = "Upload Failed";
}

function abortHandler(event) {
  _("status").innerHTML = "Upload Aborted";
}


//Customizing placeholder-label for input and textarea
$('.contact_us_form > div > textarea, .contact_us_form > div > input').focus(function(){
    setFocus($(this))
})

$('.start').click(function(){
    byLabel($(this))
})

$('.contact_us_form > div > textarea, .contact_us_form > div > input').focusout(function(){
    removeFocus($(this))
})

$('.contact_us_form > div > textarea, .contact_us_form > div > input').on('input', function(){
    removeError($(this))
})

function setFocus(item) {
    $(item).parent().find('.label-input').addClass('focus').removeClass('start')
}

function byLabel(item) {
    $('.start').click(function(){
      $(item).parent().find('.label-input').addClass('focus').removeClass('start')
      $(item).parent().find('input').focus()
    })
}

function removeFocus(item) {
  if ($(item).val() == '') {
    $(item).parent().find('.label-input').addClass('start').removeClass('focus')
  }
}

function removeError(item) {
    console.log($(item).parent().find('*[class^=contact_form_'))
    $(item).parent().find('*[class^=contact_form_]').hide()
}


$('.remove_file').click(function() {
    $('#id_file').val('');
    $('.progressbar').hide();
})

function textAreaAdjust(o) {
  o.style.height = "1px";
  o.style.height = (25+o.scrollHeight)+"px";
}
