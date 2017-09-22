function getControlGroupDiv(){
	var d = $("div:jqmData(role='header')").find("div:jqmData(role='controlgroup')");
	if (!d.length){
		//create a new controlgroup if it doesn't exist
		d =  $('<div />').attr({
				'data-type':"horizontal",
				'data-role':"controlgroup"
			}).addClass("event-detail-icon ui-btn-left");
		d.appendTo($("div:jqmData(role='header')"));
	}
	return d;
}
function isFunction(functionToCheck) {

// var getType = {};
 //return functionToCheck && getType.toString.call(functionToCheck) === '[object Function]';
 return typeof functionToCheck==="function";
}
function setupIcons(groupClass, iconList, callback){
	console.log("icon setup");
	var controlDiv = getControlGroupDiv();
	iconList.forEach(function(iconInfo){
		var text = undefined;
		var others = iconInfo['others'];
		var a;
		if (others){
			a = makeIcon(groupClass, iconInfo.icon, iconInfo.href,null, others);
		}
		else {
			a = makeIcon(groupClass, iconInfo.icon, iconInfo.href);
		}
		if (isFunction(callback)){
			console.log("callback assigned to " + a.html());
			a.click(callback);
		}
		a.appendTo(this);
	}, controlDiv);
	controlDiv.controlgroup();
	controlDiv.controlgroup("option", "type", "horizontal");
	controlDiv.children("."+groupClass).button();
	//controlDiv.controlgroup("refresh");
	//controlDiv.parent().toolbar("refresh");
	//controlDiv.parent().parent().trigger("create");
	//$("div:jqmData(role='page')").trigger("create");
	$(document).one("pagebeforechange", function(event){
		$("."+groupClass).remove();
	});
	return controlDiv;
}
function makeIcon(className, iconClass, hrefValue){
	var text = "&nbsp;";
	var noText = "ui-btn-icon-notext";
	var attrs = {href:hrefValue};
	if (arguments.length >3){
		if (arguments[3] && arguments[3]!="noText" && arguments[3]!=""){
			alert("adding text" + arguments[3]);
			text= arguments[3];
			noText = "ui-btn-icon-left";
			//attrs["data-icon"]=iconClass.split('-')[2];
		}
		if (arguments.length>4){
			for (var attrname in arguments[4]) {attrs[attrname]=arguments[4][attrname];}
		}
	}
	return $('<a />').addClass(className).addClass(iconClass).addClass(noText).attr(attrs).append(text);
}