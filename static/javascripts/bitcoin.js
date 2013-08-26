/**
 * @author zhaolin.huang 2013-07-29
 */
var bitcoin={};
/**
*/
bitcoin.requestData=function(){
	$.ajax({
		url:"queryData.htm",
		type:"post",
		data:{startTime:"2013-07-01 00:00:00",endTime:"2013-07-30 00:00:00",orignal:"BITCCHINA"},
		success:function(jsonData){
			console.log(jsonData);
		}
	})
}
bitcoin.requestData();