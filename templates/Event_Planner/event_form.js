
var dialog_instance;


function setup_accordion_headers() {
    var elems = $('input[name$="-title"]');
    var arr = new Array()
    elems.each(function(i){
	arr[i] = $(this).val()
    });
    $('h3').each(function(i) {
	$(this).find('.segment-header').text(arr[i]);
    });
}	
function segment_modified(event) {
    seg = $(this).closest('.sortables');
    seg.find('.segment-modified').text("*");
    setup_accordion_headers();
}	
function setup_accordion() {
    $( "#accordion h3" ).click(function( event ) {
	if ( stop ) {
	    //event.stopImmediatePropagation();
	    //event.preventDefault();
	    stop = false;
	}
    });	
    $( "#accordion" ).accordion({
	autoHeight:false,
	forcePlaceholderSize:true,
	forceHelperSize:true,
	navigation:true,
	collapsible:true,
	header: "> div > h3"
    })
	.sortable({
	    axis: "y",
	    handle: "h3",
	    stop: function(event, ui) {
		setTimeout('$("body").css("sortables","ui-accordion-header")', 2000);
		stop = true;
		var data = [];
		$('input[name$="order"]').each(function(i) {
		    $(this).val(i+1);
		});
		$('div[id^="sortable_"]').each(function(i) {
		    data[i] = $(this).attr("id");
		});
		
		var jqxhr = $.post("{% url 'event_order_update_view' event.id %}", JSON.stringify({'array': data}) , function(data) {
		    $("#ajax").text("order saved.").show().delay(5000).fadeOut();
		}).error(function() { alert("Connection error.") });
		if (($.browser.msie) && ($.browser.version >=6.0))
		    $('#accordion *').focus().blur();
	    },
	    //don't allow open accoridions to be dragged
	    cancel: "div[id^='sortable']:has(div.ui-accordion-content-active)"
	});
    
    ////// hide form fields that are handled automatically via javascript
    $('input[name$="order"]').hide();
    $('label[for$="order"]').hide();
    $('select[name$="-song"]').hide();
    $('label[for$="-song"]').hide();
    $('select[name$="-event"]').hide();
    $('label[for$="-event"]').hide();
    
    ////// set up accordion header names
    setup_accordion_headers();
    $('#accordion').find(":input").change(segment_modified);
}

function reset_accordion() {
    $('#accordion').accordion('destroy').sortable('destroy');
    setup_accordion();
}

function setup_activity_dialog_autocomplete() {


    $('#id_participant_name').autocomplete({
	minLength: 0,
	source: "{% url 'json_participant_list_view' %}"
    });
    $('#id_role_name').autocomplete({
	minLength: 0,
	source: "{% url 'json_role_list_view' %}"
    });
}	
var activity_button;
var delete_button;
function setup_activity_delete_button() {
    $( '.activity_delete_link' ).button({
	icons: {
	    primary: "ui-icon-trash"
	},
	text:false
    }).click(function(event) {
	delete_button = $(this);

	$( "#dialog-confirm" ).dialog({
	    resizable: false,
	    height:219,
	    width: 350,
	    modal: true,
	    autoOpen: false,
	    buttons: {
		"Delete": function() {
		    delete_button.closest('li').addClass('mark_for_delete');
		    var jqxhr = $.post(delete_button.attr('ajax_url'), [{}] , function() {
			$("#ajax").text("item deleted.").show().delay(5000).fadeOut();
			
			$(".mark_for_delete").remove();
		    })
			.error(function() { 
			    alert("error");
			    $('.mark_for_delete').removeClass('mark_for_delete');
			});
		    
		    $( this ).dialog( "close" );
		},
		Cancel: function() {
		    $( this ).dialog( "close" );
		}
	    }
	});

	$('#dialog-confirm').dialog("open");
	event.stopImmediatePropagation();
	event.preventDefault();
	return false;
    });
}

function setup_segment_form_button(){
    //$( '.segment_button' ).button('destroy');
    $( '.segment_button' ).button();
    $( '.segment_form').submit(function(e) {
	e.preventDefault(); // <-- important
	e.stopImmediatePropagation();
	this_url = $(this).attr('ajax_url');
	$(this).ajaxSubmit({
	    //target: '#id_song_list',
	    context: $(this).closest('.sortables'),
	    
	    success: function(){
	  	$(this).find('.segment-modified').text("");
	    },
	    url: this_url,
	    dataType: 'json'
	});
    });		
}   
function setup_segment_links() {
    setup_segment_form_button();
    $( '.delete_link' ).button().click(function(event) {
	delete_button = $(this);
	
	$( "#dialog-confirm" ).dialog({
	    resizable: false,
	    height:219,
	    width: 350,
	    modal: true,
	    autoOpen: false,
	    buttons: {
		"Delete": function() {
		    delete_button.closest('div.sortables').addClass('mark_for_delete');
		    var jqxhr = $.post(delete_button.attr('ajax_url'), [{}] , function() {
				$("#ajax").text("item deleted.").show().delay(5000).fadeOut();
			
				$(".mark_for_delete").remove();
				reset_accordion()
		    }).error(function() { 
			    alert("error");
			    $('.mark_for_delete').removeClass('mark_for_delete');
			});
		    
		    $( this ).dialog( "close" );
		},
		Cancel: function() {
		    $( this ).dialog( "close" );
		}
	    }
	});
	
	$('#dialog-confirm').dialog("open");
	event.stopImmediatePropagation();
	event.preventDefault();
	return false;
    });
    setup_activity_delete_button();
    $('.edit_link').hide();
    
    
    //setup activity dialog			
    $( "#dialog-add-activity" ).dialog({
	resizable: true,
	width: 640,
	modal: true,
	autoOpen: false,
	buttons: {
	    
	    "Add Activity": function() {
		$('#activity_form').ajaxSubmit({
		    success: function(data) {
			if (data.data)
			{
			    $('#dialog-add-activity-form').html(data.data);
			    setup_activity_dialog_autocomplete();
			}
			else
			    activity_button.closest(".segment-activity-buttons").siblings(".activity_div").html(data.activities);
			setup_activity_delete_button();
			$('#dialog-add-activity').dialog("close");
		    },
		    url: activity_button.attr("ajax_url")	
		});
	    },
	    Cancel: function() {
		$( this ).dialog( "close" );
	    }
	    
	}
    });	
    
    $('.add_activity_link').button().click(function(event) {
	activity_button=$(this);
	$.get(activity_button.attr('ajax_url'), function(data) {
	    $('#dialog-add-activity-form').html(data.data);
	    setup_activity_dialog_autocomplete();
	});
	$('#dialog-add-activity').dialog("open");
	event.stopImmediatePropagation();
	event.preventDefault();
	return false;
    });
    
    
    
    $('button[id^="edit_song_seg_"]').button().click(function(event) {
	
	$.get('{% url 'song_list_view' %}?xhr&options=A&page_size=5', build_dialog);
	dialog_instance=$(this).attr("instance");
	event.stopImmediatePropagation();
	event.preventDefault();
	return false;
    });	
    
}	
function add_segment_callback(data) {
    //alert(data.html);
    //$('#accordion').accordion('destroy').sortable('destroy');
    $('#accordion').append(data.html);
    reset_accordion();
    setup_segment_links();
}

function build_dialog(data) {
    var song_list = JSON.parse(data.songs_json);
    var tableContents = $('<table />');
    $.each(song_list, function(index, song) {
	var row = $('<tr />');

	var head = $('<th />');
	head.append($('<a />').attr({target:'_blank',href:song.extras.get_absolute_url}).append(song.fields.title));

	var composers = $('<td />');
	$.each(song.fields.composers, function(i, composer){
	    if (i>0) composers.append($('<br />'));
	    composers.append(composer.extras.__unicode__);
	});
	var selButton = $('<td />');
	selButton.append($('<button />').addClass("song_select").attr({song:song.pk}).append("select"));

	row.append(head);
	row.append(composers);
	row.append(selButton);

	tableContents.append(row);
    });
    
    var pagination = $('<div />').addClass("pagination");
    var links = $('<span />').addClass("page_links");
    var prevLink = $('<span />').addClass("song_prev");
    var page = data.page;
    if (page.has_previous){
	var prev_url = data.search_url+"?xhr&page_size="+page.page_size+"&page="+page.previous_page_number;
	if (data.search) prev_url+="&search="+data.search;
	if (data.option) prev_url+="&options="+data.option;
	prevLink.append($('<a />').addClass("song_dialog").addClass("song_prev").attr({
	    id:"id_prev",
	    href:prev_url
	}).append("previous"));
    }
    links.append(prevLink);
    links.append($('<span class="current" />').append("Page "+page.number+" of "+page.num_pages));
    var nextLink = $('<span />').addClass("song_next");
    if (page.has_next){
	var url_params = {
	    xhr:true,
	    page_size:page.page_size,
	    page:page.next_page_number
	};
	if (data.search) url_params["search"]=data.search;
	if (data.option) url_params["options"]=data.option;
	var next_url = data.search_url+"?"+$.param(url_params);
	nextLink.append($('<a />').addClass("song_dialog").addClass("song_next").attr({
	    id:"id_next",
	    href:next_url
	}).append("next"));
    }
    links.append(nextLink);
    pagination.append(links);
    var dialogContents = $('<div />');
    dialogContents.append(tableContents).append(pagination);

    $('#songs').html(dialogContents);	
    $('.song_dialog').click(function() {
	$.get($(this).attr("href"), build_dialog);
	return false;
    });		
    if(! $("#edit_song_dialog").dialog("isOpen")) {
	$("#edit_song_dialog").dialog("open");
    }
    $(".song_select").button().click(function() {
	song_id = $(this).attr("song");
	select_name = "segment-"+dialog_instance+"-song";
	$('select[name="'+select_name+'"]').val(song_id).change();
	select_name = "segment-"+dialog_instance+"-song-url";
	$('#'+select_name).html($(this).parent().siblings('th').html());
	$("#edit_song_dialog").dialog("close");
    });
    
}

$.widget( "ui.timespinner", $.ui.spinner, {
    options: {
	// seconds
	step: 60 * 1000 + 15,
	// hours
	page: 4
    },
    
    
    _parse: function( value ) {
	//alert("value = " + value);
	if ( typeof value === "string" ) {
            // already a timestamp
            //alert( "Number(value) = " + Number(value));
            if ( Number( value ) == value ) {
		return Number( value );
            }
            //alert(Date.parse( "01 Jan 1970 " + value));
            return Date.parse( "01 Jan 1970 " + value );
	}
	return value;
    },
    
    _format: function( value ) {
	//alert ("date: " + new Date(value));
	//alert ("format: " + Globalize.formatDate( new Date(value), { time: "medium" } ));
	//alert("_format");
	var options = {hour: "numeric", minute: "numeric"};
	//alert(":asda");
	return new Intl.DateTimeFormat("en-US", options).format(new Date(value));
	//return Date(value).toLocaleTimeString("h:mm tt");
    }
});
{% if flavor != "mobile" %}
$(function() {
    $("#edit_song_dialog").dialog({
	modal:true,
	autoOpen:false,
	width: 640
    });
    
    
    
    
    var stop = false;
    
    setup_accordion();
    $("#id_date_0").datepicker();
    $("#id_date_1").timespinner();
    
});
{% endif %}

var wait = false;
var queued_submit = false;
function autosubmit(eventObject) {
    var TIMEOUT = 2000;
    
    var options = {
	success: build_dialog,
	url: '{% url 'song_list_view' %}?xhr&page_size=5',
	dataType: 'json'
    }
    if (!wait) {
	wait=true;
	$( '#search_form' ).ajaxSubmit(options);
	window.setTimeout(function() {
	    wait = false;
	    if (queued_submit) {
		queued_submit=false;
		$( '#search_form' ).ajaxSubmit(options);		
	    }
	}, TIMEOUT);
    }
    else 
	queued_submit=true;
}


$( document ).ready( function() {
    {% if flavour == "mobile" %}

    {% else %}
    //$('#accordion').sortable("option", "cancel", "div[id^='sortable']:has(div.ui-accordion-content-active)");
    $('#accordion').sortable();
    var options = {
	success: build_dialog,
	url: '{% url 'song_list_view' %}?xhr&page_size=5',
	dataType: 'json'
    }
    
    $( '#search_form' ).bind('submit', function(e) {
	e.preventDefault(); // <-- important
	$(this).ajaxSubmit(options);
    });
    
    $( '#id_search' ).keyup(autosubmit);
    $( '#id_options' ).change(autosubmit);
    {% if event %}
    $( '#add_segment' ).click(function() {
	$.get('{% url 'segment_create_view' event.id %}', add_segment_callback)
	    .error(function(data) { //alert("error"); 
	    });
	return false;
    });
    $( '#add_songsegment' ).click(function() {
	$.get('{% url 'songsegment_create_view' event.id %}', add_segment_callback)
	    .error(function(data) { alert("error"); 
				  });
	return false;
    });
    {% endif %}
    setup_segment_links()
    $("#ajax").ajaxError(function(event, request, settings){
  	$(this).append("<li>Error requesting page " + settings.url + "</li>");
  	$(this).append(request.responseXML);
    });
    {% endif %}
});

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


