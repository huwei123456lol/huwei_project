$(function(){
	var i = 1;
	$("span.addattribute").click(function(){
		var addAttribute = document.getElementById("addAttribute");
		// 获得原有的Html代码
		var previousHtml = addAttribute.innerHTML;
		addAttribute.innerHTML = previousHtml+'<p><label>属性名'+i+':</label><input type="text" name="attribute'+i+'" placeholder="最好使用英文"/></p><p><label>属性类型'+i+':</label><input type="text" name="texttype'+i+'" placeholder="属性类型"/></p><p><label>长度'+i+':</label><input type="number" name="length'+i+'" /></p><p><label>是否为空'+i+':</label><input type="radio" name="isNull'+i+'" value="null"/>空<input type="radio" name="isNull'+i+'" value="not null"/>非空</p>';
		i = i+1;
		var count = document.getElementById("attributeCount");
		count.value = i;
	});
}());