<?php
class Learnfilter extends Plugin {
	private $link;
	private $host;
	private $curl_learnfilter;

	function init($host) {
		$this->link = $host->get_link();
		$this->host = $host;
		$this->curl_learnfilter = $curl_learnfilter;
		$this->curl_learnfilter = curl_init() ;
		curl_setopt($this->curl_learnfilter, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($this->curl_learnfilter, CURLOPT_FOLLOWLOCATION, true);

		//$host->add_hook($host::HOOK_ARTICLE_BUTTON, $this);
		$host->add_hook($host::HOOK_PREFS_TAB, $this);
	}

	function about() {
		return array(0.1,
				"Filter articles using personal ratings of articles or tags extrated from them.",
				"Jiří Procházka");
	}
	function save() {
		$learnfilter_url = db_escape_string($this->link, $_POST["learnfilter_url"]);
		$this->host->set($this, "Learnfilter_URL", $learnfilter_url);
		echo "Value Learnfilter URL set to $learnfilter_url<br/>";
	}
	function get_js() {
		return file_get_contents(dirname(__FILE__) . "/learnfilter.js");
	}

	function urlsafe_b64encode($data) {
		//return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
		return strtr(base64_encode($data), '+/', '-_');
	}
	function urlsafe_b64decode($data) {
		//return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '=', STR_PAD_RIGHT));
		return base64_decode(strtr($data, '-_', '+/'));
	}
	// $_SESSION['uid'] or $_SESSION['name'] as user ID

	/*function hook_article_button($line) {
		$article_id = $line["id"];

		$rv = "<img src=\"plugins/learnfilter/learnfilter.png\"
			class='tagsPic' style=\"cursor : pointer\"
			onclick=\"shareArticleToLearnfilter($article_id)\"
			title='".__('Send article to Learnfilter')."'>";

		return $rv;
	}*/

	/*function getInfoOld() {
		$id = db_escape_string($this->link, $_REQUEST['id']);

		$result = db_query($this->link, "SELECT title, link
				FROM ttrss_entries, ttrss_user_entries
				WHERE id = '$id' AND ref_id = id AND owner_uid = " .$_SESSION['uid']);

		if (db_num_rows($result) != 0) {
			$title = truncate_string(strip_tags(db_fetch_result($result, 0, 'title')),
					100, '...');
			$article_link = db_fetch_result($result, 0, 'link');
		}
	
		$learnfilter_url = $this->host->get($this, "Learnfilter_URL");
		$learnfilter_api = $this->host->get($this, "Learnfilter_API");

		print json_encode(array("title" => $title, "link" => $article_link,
					"id" => $id, "learnfilterurl" => $learnfilter_url, "learnfilterapi" => $learnfilter_api));		
	}

	function getInfo() {
		$id = db_escape_string($this->link, $_REQUEST['id']);

		$result = db_query($this->link, "SELECT title, link
				FROM ttrss_entries, ttrss_user_entries
				WHERE id = '$id' AND ref_id = id AND owner_uid = " .$_SESSION['uid']);

		if (db_num_rows($result) != 0) {
			$title = truncate_string(strip_tags(db_fetch_result($result, 0, 'title')),
					100, '...');
			$article_link = db_fetch_result($result, 0, 'link');
		}
	
		$learnfilter_url = $this->host->get($this, "Learnfilter_URL");
		$learnfilter_api = $this->host->get($this, "Learnfilter_API");
/*		$curl_learnfilter = curl_init() ;
		curl_setopt($curl_learnfilter, CURLOPT_URL, "$learnfilter_url/learnfilter-api.php?signature=$learnfilter_api&action=shorturl&format=simple&url=".urlencode($article_link)."&title=".urlencode($title)) ;
		curl_setopt($curl_learnfilter, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl_learnfilter, CURLOPT_FOLLOWLOCATION, true);
		$short_url = curl_exec($curl_learnfilter) ;
		curl_close($curl_learnfilter) ;*/ 
        /*        curl_setopt($this->curl_learnfilter, CURLOPT_URL, "$learnfilter_url/learnfilter-api.php?signature=$learnfilter_api&action=shorturl&format=simple&url=".urlencode($article_link)."&title=".urlencode($title)) ;
                $short_url = curl_exec($this->curl_learnfilter) ;

		print json_encode(array("title" => $title, "link" => $article_link,
					"id" => $id, "learnfilterurl" => $learnfilter_url, "learnfilterapi" => $learnfilter_api, "shorturl" => $short_url));		
	}*/

	function hook_prefs_tab($args) {
		if ($args != "prefPrefs") return;

		print "<div dojoType=\"dijit.layout.AccordionPane\" title=\"".__("Learnfilter")."\">";

		print "<br/>";

		$learnfilter_url = $this->host->get($this, "Learnfilter_URL");
		//$learnfilter_api = $this->host->get($this, "Learnfilter_API");
		print "<form dojoType=\"dijit.form.Form\">";

		print "<script type=\"dojo/method\" event=\"onSubmit\" args=\"evt\">
			evt.preventDefault();
		if (this.validate()) {
			console.log(dojo.objectToQuery(this.getValues()));
			new Ajax.Request('backend.php', {
parameters: dojo.objectToQuery(this.getValues()),
onComplete: function(transport) {
notify_info(transport.responseText);
}
});
}
</script>";

		print "<input dojoType=\"dijit.form.TextBox\" style=\"display : none\" name=\"op\" value=\"pluginhandler\">";
		print "<input dojoType=\"dijit.form.TextBox\" style=\"display : none\" name=\"method\" value=\"save\">";
		print "<input dojoType=\"dijit.form.TextBox\" style=\"display : none\" name=\"plugin\" value=\"learnfilter\">";
		print "<table width=\"100%\" class=\"prefPrefsList\">";
		print "<tr><td width=\"40%\">".__("Learnfilter prefextract service URL")."</td>";
		print "<td class=\"prefValue\"><input dojoType=\"dijit.form.ValidationTextBox\" required=\"1\" name=\"learnfilter_url\" regExp='^(http|https)://.*' value=\"$learnfilter_url\"></td></tr>";
		//print "<tr><td width=\"40%\">".__("Learnfilter API Key")."</td>";
		//print "<td class=\"prefValue\"><input dojoType=\"dijit.form.ValidationTextBox\" required=\"1\" name=\"learnfilter_api\" value=\"$learnfilter_api\"></td></tr>";
		print "</table>";
		print "<p><button dojoType=\"dijit.form.Button\" type=\"submit\">".__("Save")."</button>";

		print "</form>";

		print "</div>"; #pane

	}

}
?>
