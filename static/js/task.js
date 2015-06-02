var signUp = $('#signUp'),
	email = $('#email'),
	lineId = $('#lineId'),
	scopeid = $('#scopeid'),
	popUp = $('.popUp'),
	tip = $('.popUp .tip'),
	register = $('.register'),
    url = $('#url').val();

if (!window.urlOpener) {
    $('.enter').add('.close').hide();
}

function Send() {

	if (email.val() == "") {
		popUp.css('display', 'block');
		tip.html('郵箱不能為空');
        $('.enter').add('.close').hide();
		return;
	}
	if (/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(email.val()) == false) {
		popUp.css('display', 'block');
		tip.html('郵箱格式不正確，請重新輸入');
        $('.enter').add('.close').hide();
		return;
	}

	$.ajax({
		type: 'POST',
		url: '',
		data: {email: email.val(), lineId: lineId.val(), scopeid: scopeid.val()},
		dataType: 'json',
		success: function(data) { // return {value: 1||2}  1---报名成功 ; 2----名额已满
			popUp.css('display', 'block');
			if (data.value === 1) {
				tip.html('恭喜妳，報名成功');
				register.css('display', 'none');
				$('.success').css('display', 'block');
				$('.full').css('display', 'none');
                $('.enter').add('.close').show();
			}
			else if (data.value === 0) {
				tip.html('名額已滿，請保持關注新任務');
				register.css('display', 'none');
				$('.success').css('display', 'none');
				$('.full').css('display', 'block');
                $('.enter').add('.close').hide();
			}
		},
		error: function(){
			popUp.css('display', 'block');
			tip.html('網絡出錯，稍後再試哦');
            $('.enter').add('.close').hide();
		}
	})
}

signUp.bind('click', function () {
	Send();
})
$('.bg').add('.close').bind('click', function() {
	popUp.css('display', 'none');
})
$('.enter').click(function() {
    window.urlOpener.openUrl(url);
});
