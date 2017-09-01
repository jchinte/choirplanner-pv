//Add a segment
//shift up/down
//

//globals
var currentInstance; //contains form id of the clicked "choose song" button
var savedScroll=0;   //scroll of the page before the button was clicked
var currentScroll = 0; // scroll of the page before adding to the #autocomplete div
//$(document).one("pageload", function(){
	//$("#id_date_0").attr("data-role","date");
//var date = new Date(Date($("#id_date_0").attr("data-role", "date")));
console.log($("#id_date_0").val());
//var date = new Date(Date($("#id_date_0").val()));
//console.log(date);
//	var m = "0"+date.getMonth();
//	var d = "0"+date.getDay();
//	var datestr = "" + date.getFullYear()+"-"+ m.substr(m.length-2) + "-"+d.substr(d.length-2);
	
	$("#id_date_0").attr("type","date").attr("data-clear-btn","false");
	var date = new Date("2000-01-01 "+$("#id_date_1").val());
	var s = "0"+date.getHours();
	var time = s.substr(s.length-2) +":"+date.getMinutes();
	$("#id_date_1").val(time).attr("type","time").attr("data-clear-btn","false");
//});

$(document).one("pagebeforeshow", function(){
	console.log("event form icon setup");
	var icons = [];
	{% if event %}
	icons.push({
			icon:"ui-icon-plus",
			href:"{% url 'songsegment_create_view' event.id %}"
		});
	setupIcons("event-form-icon", icons, addSong);
	{% endif %}
	icons = [];
	icons.push({
		icon:"ui-icon-delete",
		href:"#",
		others:{
					"data-rel":"back",
					"data-inline":"true",
					style:"padding:0",		
		       }
		
	});
	icons.push({
		icon:"ui-icon-home", 
		href:"{% url 'event_list_view' %}"
	});
	setupIcons("event-form-icon", icons);	
	var $forms = $('.segment_form');
	$forms.each(setupForm);
});
{% if event %}
function addSong(e){
	e.preventDefault();
	console.log("add song");
	$.get('{% url 'songsegment_create_view' event.id %}', addSongCallback)
	    .error(function(data) { alert("error"); 
				  });
	return false;
}
{% endif %}
function addSongCallback(data) {
    //alert(data.html);
    //$('#accordion').accordion('destroy').sortable('destroy');
    var newForm = $(data.html);
    //newForm.collapsible();
    //$("div:jqmData(role='page')").trigger("create");
    $('#formSet').append(newForm).trigger("create");
    //reset accordion
    setup_accordion_headers();
    //setup buttons and events
    setupForm(0, newForm.find(".segment_form"));
}


$(document).on("pageinit", function() {


	//AJAX scroll handler
	//console.log("add scroll handler");
	var barHeight = $("div:jqmData(role='header')").height() + $("div:jqmData(role='footer')").height();
	
	$(".ui-panel-inner").on("scrollstop",function(){
		console.log("scroll. doc height="+$(".ui-panel-inner").height());
		console.log("scroll panel height = "+$('#autocomplete').height());
		console.log('scroll window height = ' + eval($(window).height()-barHeight));
		console.log('scrolled above: '+$(window).scrollTop());
		console.log('panel scrolled above: '+$("#chooseSongDialog div.ui-panel-inner").scrollTop());
		console.log('bar height = ' + barHeight);
		if ($("#chooseSongDialog div.ui-panel-inner").scrollTop()>=$('#autocomplete').height() + barHeight - $(window).height()){
			console.log("bottom of scroll reached.");
			$('#moreSongs').click();
			currentScroll = $(window).scrollTop();
		}
	});
	//console.log("add scroll handler");

	$('#chooseSongDialog').on("panelclose", function(event, ui){
		//savedScroll is set on opening the panel.
		console.log("panel closed" + savedScroll);
		savedScroll&&$.mobile.silentScroll(savedScroll);
		
	});
	

	setupAutocomplete();
	var mainFormInputs = $('#id_form').find(":input");
    {% if event %}
    /*
    mainFormInputs.keyup(segment_modified);
    mainFormInputs.keyup(segment_modified);
    */
    {% endif %}
    /*
    var thisURL = $("#{{ page_id }}").attr("data-url");
    $("#id_form").attr("action", thisURL);
    $("#id_form").attr("ajax_url", thisURL);*/
    {% if event %}
    /*
	$("#id_form").submit(function(e){
		e.preventDefault();
		e.stopImmediatePropagation();
		console.log('main form submit');
		this_url = $(this).attr('ajax_url');
		console.log( "url: "+this_url);
		$(this).ajaxSubmit({
			context: $(this),
			success: function(){
				
			},
			url: this_url,
			dataType: 'json'
		});
	});*/	
	{% endif %}
	console.log("END IF PAGEINIT");

});

function deleteSegment(e){
	e.stopPropagation();
	e.stopImmediatePropagation();
	e.preventDefault();
	$('#deleteDialog').popup().popup("open");
	var $segment = $(this).closest('div.sortables');
	var $delete_button = $(this);
	console.log("deleting "+$segment.html());
	$('#confirmDelete').one('click', function(){
		console.log("deleting");
		$segment.addClass("mark_for_delete");
		//don't save data for a segment that will be deleted
		var $form = $segment.find('form');
    	if ($form.attr('timeoutID')){
    		console.log("cleared timeout");
    		window.clearTimeout(Number($form.attr('timeoutID')));
    		$form.attr('timeoutID', '');
    	}		
    	
		var jqxhr = $.post($delete_button.attr('ajax_url'), [{}] , function() {
			$("#ajax").text("item deleted.").show().delay(5000).fadeOut();
			console.log($(".mark_for_delete"));
			$(".mark_for_delete").remove();
			//$("#formSet").colllapsibleset().collapsibleset("refresh");
			//
		    }).error(function() { 
			    alert("error");
			    $('.mark_for_delete').removeClass('mark_for_delete');
			});
	});
}

function setupForm(index, element){
	console.log("setup"+element);
	var $sortable = $(element).closest(".sortables");
	$sortable.find(".buttonUp").click(function(e){
		e.stopPropagation();
		e.stopImmediatePropagation();
		e.preventDefault();
		var $prev = $sortable.prev();
		if ($prev.length>0){
			$prev.before($sortable);
			var temp = $sortable.find('input[id$="-order"]').val();
			$sortable.find('input[id$="-order"]').val($prev.find('input[id$="-order"]').val());
			$prev.find('input[id$="-order"]').val(temp);
			$sortable.find('form').submit();
			$prev.find('form').submit();
		}
		$sortable.collapsible("collapse");
		$prev.collapsible("collapse")
	});
	$sortable.find(".buttonDown").click(function(e){
		e.stopPropagation();
		e.stopImmediatePropagation();
		e.preventDefault();
		var $next = $sortable.next();
		if ($next.length>0){
			$next.after($sortable);
			var temp = $sortable.find('input[id$="-order"]').val();
			$sortable.find('input[id$="-order"]').val($next.find('input[id$="-order"]').val());
			$next.find('input[id$="-order"]').val(temp);
			$sortable.find('form').submit();
			$next.find('form').submit();
		}
		$sortable.collapsible("collapse");
		$next.collapsible("collapse")
	});	
	
	$(element).submit(function(e){
		e.preventDefault();
		e.stopImmediatePropagation();
		console.log('form submit');
		this_url = $(this).attr('ajax_url');
		console.log( "url: "+this_url);
		$(this).ajaxSubmit({
			context: $(this).closest('.sortables'),
			success: function(){
				$(this).find('.segment-modified').text("");
			},
			url: this_url,
			dataType: 'json'
		});
	});


	$sortable.find('.btnChooseSong').on("click", function(e){
		e.stopPropagation();
		e.stopImmediatePropagation();
		e.preventDefault();
		var target = $(this);
		savedScroll = $(window).scrollTop();
	    $("#chooseSongDialog").panel("open");
	    $("#autocomplete-input").trigger("keyup");
	    currentInstance=target.attr("instance");
	    currentScroll = 0;
	    
	    console.log("button clicked. scroll="+savedScroll);
	});
	$(element).find('label[for$="-song"]').parent().hide();
	$(element).find('label[for$="-event"]').parent().hide();
	$(element).find('label[for$="-event"]').parent().hide();
	$(element).find('label[for$="-order"]').parent().hide();
    //jquery mobile - hide parent, since the button gets wrapped in a div
    $(element).find('.segment_button').parent().hide();
    
    //save elements on edit
    var formInputs = $(element).find(":input");
    formInputs.keyup(segment_modified);
    formInputs.change(segment_modified);
    $sortable.find('select').change(segment_modified);
    $(element).closest('.sortables').find(".delete_button").click(deleteSegment);   
    console.log("add delete segment handler"); 
}
var autocompleteTimeoutID;
function setupAutocomplete(){	
    $("#autocomplete-input").keyup(function(){
    	console.log("autocomplete keyup triggered");
		var $listview = $("#autocomplete"),
		    $input = $(this),
		    value = $input.val(),
		    html="";
		$listview.html("");
		
		if (value==""  ||  value.length>2) {
			
		    $listview.html("<li id='moreSongs' start=0 page=20><div class='ui-loader'><span class='ui-icon ui-icon-loading'></span></div></li>");
		    $('#moreSongs').click(function(e){
							console.log('click');
						    delayLoadSongs(500);
				});
		    
		    $listview.listview("refresh");
		    //call the remote procedure
		    function loadSongs(){
		    	autocompleteTimeoutID = undefined;
		    	$('#moreSongs').html("<div class='ui-loader'><span class='ui-icon ui-icon-loading'></span></div>")
			    $.ajax({
			    	url: "{% url 'json_songlist_view' %}",
			    	dataType: "json",
			    	data: {
			    		limit:$('#moreSongs').attr('page'),
			    		start:$('#moreSongs').attr('start'),
			    		//options:"A",
			    		search:value,
			    	}
			    }).then(function(response){
			    	$lastSong = $('#moreSongs');
					//set up things
					var songs_json = JSON.parse(response.songs_json);
					$.each(JSON.parse(response.songs_json), function (i, val) {
					    var item = $('<li />');
					    var link = $('<a href="#"/>').attr("sID", val.pk).attr("instance",currentInstance).
					          attr("url", val.extras.get_absolute_url).text(val.fields.title);
					    console.log(link[0]);
					    link.click({song:val.pk,instance:currentInstance}, selectSong);
					    item.append(link);
					    $lastSong.before(item);
					});
					if (songs_json.length+eval($('#moreSongs').attr('start'))>=response.count){
						$('#moreSongs').remove();
					}
					else {
				    	$lastSong.attr('start', eval($lastSong.attr('start'))+eval($lastSong.attr('page'))).text("More");
					}

				    $listview.listview("refresh");
				    $listview.trigger("updatelayout");
				    $.mobile.silentScroll(currentScroll);
			    });
		    }
		    function delayLoadSongs(delay){
		    	if (delay==0){
		    		loadSongs();
		    	}
		    	else {
			    	if (!delay) delay=500;
				    if (autocompleteTimeoutID){
				    	window.clearTimeout(autocompleteTimeoutID);
				    	autocompleteTimeoutID = undefined;
				    }
				    autocompleteTimeoutID = window.setTimeout(loadSongs, 200);
				}
			}
			delayLoadSongs();
		}
    });
}
    
function segment_modified(event) {
	console.log("asdf");
    seg = $(this).closest('form');
    //seg.find('.segment-modified').text("*");
    if (seg.attr('timeoutID')){
    	window.clearTimeout(Number(seg.attr('timeoutID')));
    }
    var timeoutID = window.setTimeout(function(){
    	timeoutID = undefined;
    	seg.submit();
    }, 1000);
  	seg.attr('timeoutID', timeoutID);  
    setup_accordion_headers();
}



function selectSong(e){
	console.log("song selected");
	console.log(e);
    var songId = e.data.song;
    var selectId = "segment-"+e.data.instance+"-song";
    var link = $('<a />').attr("href", $(this).attr("url")).text($(this).text());
    var spanLinkID = "#segment-"+e.data.instance+"-song-url";
    console.log(spanLinkID);
    $(spanLinkID).html("").append(link).closest("form").submit();
    $("#chooseSongDialog").panel("close");
    $('select[name="'+selectId+'"]').val(songId).change();
    $(spanLinkID).closest(".sortables").collapsible("collapse");
    
    //setup_accordion_headers();
}




function setup_accordion_headers() {
    $('h4').each(function(i) {
	$(this).find('.segment-header').html($(this).parent().find('input[name$="-title"]').val() + " - " + $(this).parent().find('.selectedSong').html());
    });
}
setup_accordion_headers();

$(document).ajaxSend(function(event, xhr, settings) {
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
    function sameOrigin(url) {
	// url could be relative or scheme relative or absolute
	var host = document.location.host; // host + port
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	// Allow absolute or scheme relative URLs to same origin
	return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
	    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
	    // or any other URL that isn't scheme relative or absolute i.e relative.
	    !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
	xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

