var init_bid = function(currentUser){
	navigator.id.watch({
		loggedInUser: currentUser,
		onlogin: function(assertion) {
			$.ajax({ 
				type: 'POST',
				url: '/auth/login', // This is a URL on your website.
				data: {assertion: assertion},
				success: function(res, status, xhr) { 
					window.location.reload();
					//console.log(res, status, xhr);
				},
				error: function(xhr, status, err) { 
					console.log("Login failure: " + err); 
				}
			});
		},
		onlogout: function() {
			$.ajax({
				type: 'POST',
				url: '/auth/logout', // This is a URL on your website.
				success: function(res, status, xhr) { 
					//console.log(res, status, xhr);
					window.location.reload(); 
				},
				error: function(xhr, status, err) { 
					console.log("Logout failure: " + err); 
				}
			});
		}
	});

}
