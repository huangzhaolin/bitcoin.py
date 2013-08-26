/**
 * @author zhaolin.huang 2013-1-10
 */
String.prototype.trim = function() {
	return this.replace(/(^[\s]*)|([\s]*$)/g, "");
};
String.nullAble = function(string) {
	return string?string:"";
};