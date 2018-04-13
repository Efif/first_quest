function submitForm(act) {
	document.main.mode.value = act;
	document.main.submit();
	return false;
}

function changeForm(act, character) {
	var scroll_top = $(window).scrollTop();
	document.main.scroll_top.value = scroll_top;
	document.main.target_character.value = character;
	return submitForm(act);
}

function submitMenu(act) {
	document.menu.mode.value = act;
	document.menu.submit();
	return false;
}

function submitSearch(act) {
	if (document.menu.search.value == "") {
		alert("検索条件を入力して下さい。");
		return false;
	}
	return submitMenu(act);
}

function submitEdit(act) {
	if (document.main.session_password.value == "") {
		alert("編集用パスワードを入力して下さい。");
		return false;
	}
	return submitForm(act);
}

function submitViewPassword(act) {
	if (document.main.view_password.value == "") {
		alert("閲覧用パスワードを入力して下さい。");
		return false;
	}
	return submitForm(act);
}

function viewCharacter(id) {
	window.open("http://lfds.daynight.jp/observatory/?mode=view_character&character_id=" + id, "_blank")
	return false;
}

function viewPrivateCharacter(id, password) {
	window.open("http://lfds.daynight.jp/observatory/?mode=view_character&character_id=" + id + "&password=" + password, "_blank")
	return false;
}

function viewSession(id) {
	window.open("http://lfds.daynight.jp/observatory/?mode=view_session&session_id=" + id, "_blank")
	return false;
}

function viewPrivateSession(id, password) {
	window.open("http://lfds.daynight.jp/observatory/?mode=view_session&session_id=" + id + "&password=" + password, "_blank")
	return false;
}

function changePublicType() {
	if (document.main.public_type_limited.checked) {
		document.main.view_password.disabled = "";
	} else {
		document.main.view_password.disabled = "true";
	}
}

$(function(){
	$('#password-form').on('show.bs.modal', function (event) {
		var button = $(event.relatedTarget);
		var recipient = button.data("name");
		document.main.session_id.value = recipient;
	});

	var nua = navigator.userAgent;
	var isAndroid = (nua.indexOf('Mozilla/5.0') > -1 && nua.indexOf('Android ') > -1 && nua.indexOf('AppleWebKit') > -1 && nua.indexOf('Chrome') === -1);
	if (isAndroid) {
		$('select.form-control').removeClass('form-control').css('width', '100%');
	}
});
