/**
 * @authoer:zhaolinhuang create:2012-12-5
 */
Date.prototype.format = function(formatString) {
	var that=this;
	var formatMapper = {
		"%Y": this.getFullYear(),
		"%m": this.getMonth() + 1,
		"%d": this.getDate(),
		"%H": this.getHours(),
		"%M": this.getMinutes(),
		// Ӣ�ĵ��·�
		"%Em": this.toString().split(" ")[1],
		"%s": this.getSeconds(),
		"%S": this.getMilliseconds(),
		"%w": this.getDay(),
		"%U": (function(day) {
			return {
				0: "����",
				1: "��һ",
				2: "�ܶ�",
				3: "����",
				4: "����",
				5: "����",
				6: "����"
			}[day];
		})(this.getDay()),
		"%u": function() {
			return parseInt(((that.getTime() - new Date(that.format("%Y-01-01")).getTime()) / (1000 * 24 * 60 * 60) + 1) / 7) + 1;
		}
	};
	if (formatString) {
		try {
			for (var d in formatMapper) {
				var re = new RegExp(d, 'g');
				formatString = formatString.replace(
				re, (String(formatMapper[d]).length == 1 ? ("0" + formatMapper[d]) : formatMapper[d]));
			}
		} catch (e) {
			console.log("FORMAT DATE ERROR:" + e);
		}
	}
	return formatString;
};
/**
 * sleep�뼶
 */
Date.prototype.sleep = function(millSecond) {
	var nowTime = new Date().getTime();
	var compareTime = nowTime + millSecond;
	while (new Date().getTime() < compareTime) {

	}
	return;
};
/**
 * ��:2012��12��18�� 00:00
 */
Date.prototype.datetime2FullCN = function() {
	return this.format("%Y��%m��%d�� %H:%M");
};
/**
 * ��:2012-12-18 00:00
 */
Date.prototype.datetime2FullMin = function() {
	return this.format("%Y-%m-%d %H:%M");
};
/**
 * ��2012-12-18 00:00:00
 *
 * @returns
 */
Date.prototype.datetime2SimpleFormat = function() {
	return this.format("%Y-%m-%d %H:%M:%s");
};
/**
 * ʱ�� ������+������-
 */
Date.prototype.changeTimezone = function(timeZone) {
	var times = this.getTime();
	var EnglandTime = times + this.getTimezoneOffset() * 60 * 1000;
	var yourTimeZoneTime = EnglandTime + timeZone * 60 * 60 * 1000;
	this.setTime(yourTimeZoneTime);
	return this;
};
/**
 * �뼶
 *
 * @param second
 */
Date.prototype.changeTime = function(second) {
	var nowTime = this.getTime();
	this.setTime(nowTime + second * 1000);
	return this;
};
/**
 * ������������Ϊ����
 *
 * @param dayNum
 */
Date.prototype.addDays = function(dayNum) {
	var times = dayNum * 24 * 60 * 60 * 1000;
	this.setTime(this.getTime() + times);
	return this;
};
/**
 * ���뼶ʱ��Ա�
 * -1 С��
 * 0 ����
 * 1 ����
 */
Date.prototype.compareTime = function(compareDate) {
	if (compareDate instanceof Date) {
		if (compareDate.getTime() > this.getTime()) {
			return -1;
		} else if (compareDate.getTime() == this.getTime()) {
			return 0;
		} else {
			return 1;
		}
	} else {
		throw {
			name: "��������쳣",
			message: compareDate + "������ȷ��Date����"
		};
	}
};
/**
 * ֻ�Ƚ�����
 *
 * @param compareDate
 */
Date.prototype.compareDay = function(compareDate) {
	if (compareDate instanceof Date) {
		var thisDate = new Date(this.format("%Y-%m-%d 00:00:00"));
		compareDate = new Date(compareDate.format("%Y-%m-%d 00:00:00"));
		return thisDate.compareTime(compareDate);
	} else {
		throw {
			name: "��������쳣",
			message: compareDate + "������ȷ��Date����"
		}
	};
};