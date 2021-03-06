/**
 * @author zhaolin.huang 2013-07-29
 */
var bitcoin = {};
bitcoin.tradeDatas = {}
/**
 */
bitcoin.requestData = function () {
    $.ajax({
        url: "queryData.htm",
        type: "post",
        data: {startTime: new Date().addDays(-1).datetime2SimpleFormat(), endTime: new Date().datetime2SimpleFormat(), orignal: "BITCCHINA"},
        success: function (jsonData) {
            bitcoin.tradeDatas["btcchina"] = null;
            bitcoin.tradeDatas["btcchina"] = JSON.parse(jsonData);

            $.ajax({
                url: "queryData.htm",
                type: "post",
                data: {startTime: new Date().addDays(-1).datetime2SimpleFormat(), endTime: new Date().datetime2SimpleFormat(), orignal: "BITCCHINA"},
                success: function (jsonData) {
                    bitcoin.tradeDatas["mtgox"] = null;
                    bitcoin.tradeDatas["mtgox"] = JSON.parse(jsonData);
                    bitcoin.drawPriceChart()
                }});
        }});
};
bitcoin.drawPriceChart = function () {
    function chartData(datas) {
        var chartDatas = []
        for (var tradeDataIndex in datas) {
            tradeData = datas[tradeDataIndex];
            chartDatas.push([tradeData.date_time, tradeData.price])
        }
        return chartDatas;
    }

    if ($("#chart01").size() < 1) {
        $("#trade_chart").append("<div style='float:left;width:45%' id='chart01'></div>");
    }
    if ("btcchina" in bitcoin.tradeDatas && bitcoin.tradeDatas.btcchina && "mtgox" in bitcoin.tradeDatas && bitcoin.tradeDatas.mtgox) {
        console.log("draw price chart")
        $("#chart01").highcharts({
            chart: {
                type: 'spline'
            },
            plotOptions: {
                spline: {
                    lineWidth: 2,
                    states: {
                        hover: {
                            lineWidth: 3
                        }
                    },
                    marker: {
                        enabled: false
                    }
                }
            },
            title: {
                text: 'BTCCHINA AND MTGOX'
            }, xAxis: {
                type: 'datetime',
                dateTimeLabelFormats: { // don't display the dummy year
                    minute: "%A, %b %e, %H:%M",
                    hour: "%A, %b %e, %H:%M"
                }
            },
            series: [
                {
                    name: 'btcchina',
                    data: chartData(bitcoin.tradeDatas.btcchina)

                },
                {
                    name: 'mtgox',
                    data: chartData(bitcoin.tradeDatas.mtgox)
                }
            ]
        });
    }
}
$(document).ready(function () {
    setInterval(bitcoin.requestData, 10000);
});