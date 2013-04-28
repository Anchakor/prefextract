	function learnfilterModRating(kwmod, val, articleHash) {
	try {
		var query = { op: 'pluginhandler', plugin: 'learnfilter', method: 'modRating', mod: kwmod, value: val, hash: articleHash };
		new Ajax.Request("backend.php",	{
			parameters: query,
			method: 'post',
			onSuccess: function(transport) {
				dialog = new dijit.Dialog({
					title: __("Keyword rating modified"),
					style: "width: 200px",
					content: transport.responseText,
				});
				dialog.show();

			} });
	} catch (e) {
		exception_error("learnfilterArticle", e);
	}
	}	
	function learnfilterShow(id) {
		var el = document.getElementById(id);
		el.style.display = (el.style.display != 'none' ? 'none' : '' );
	}

