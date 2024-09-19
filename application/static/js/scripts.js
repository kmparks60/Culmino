$(document).ready(function() {
	function checkPasswordMatch() {
		var password = $('#password').val();
		var confirmPassword = $('#confirm_password').val();

		if (password === confirmPassword && password.length > 0) {
				$('#password_error').text('');
		} else {
				$('#password_error').text('Passwords do not match.');
		}
}

	$('#password, #confirm_password').on('keyup', checkPasswordMatch);

	$('#togglePassword').on('click', function() {
		var passwordField = $('#password');
		var type = passwordField.attr('type') === 'text' ? 'password' : 'text';
		passwordField.attr('type', type);
		$(this).toggleClass('fa-eye-slash fa-eye');
	});
});
