	function shareArticleToLearnfilter(id) {
	try {
		var query = "?op=pluginhandler&plugin=learnfilter&method=getInfo&id=" + param_escape(id);

		var d = new Date();
	        var ts = d.getTime();


		new Ajax.Request("backend.php",	{
			parameters: query,
			onSuccess: function(transport) {
				var ti = JSON.parse(transport.responseText);
				var share_url_query = "?signature=" + ti.learnfilterapi + "&action=shorturl&format=simple&url=" + param_escape(ti.link) + "&title=" + param_escape(ti.title);
				dialog = new dijit.Dialog({
					id: "LearnfilterShortLinkDlg"+ts,
					title: __("Youlrs Shortened URL"),
					style: "width: 200px",
					//content: "<iframe src='"+ti.learnfilterurl + "/learnfilter-api.php" + share_url_query+"' frameborder='0' allowtransparency='true' scrolling='no' height='40px' width='190px'></iframe>",
					content: '<p align=center>' + ti.shorturl + '<br/><a href="http://twitter.com/share?_=' + ts + '&text=' + param_escape(ti.title) +
                                        '&url=' + param_escape(ti.shorturl) + '"><img src="/plugins/learnfilter/tweetshare.png"/></a><br/><a href="http://www.facebook.com/sharer.php?u=' + param_escape(ti.shorturl) + '"><img src="/plugins/learnfilter/fbshare.png" border=0/></a></p>',
					});
				dialog.show();
			} });

	} catch (e) {
		exception_error("learnfilterArticle", e);
	}
	}
