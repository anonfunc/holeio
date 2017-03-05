%rebase base
<!DOCTYPE html>
<h1>Hole.io Config</h1>
<form action="config" method="post">
<fieldset>
<legend>Web Configuration</legend>
<label for="Host">Host</label><input type="text" name="host" id="host" value="{{host}}"> <br>
<label for="Root">Root</label><input type="text" name="root" id="root" value="{{root}}"> <br>
</fieldset>
<fieldset>
<legend>OAuth Configuration</legend>
<label for="client_id">Client ID</label><input type="text" name="client_id" id="client_id" value="{{client_id}}"> <br>
<label for="client_secret">Client Secret</label><input type="text" name="client_secret" id="client_secret" value="{{client_secret}}"> <br>
<p>With a set client id and secret, visit <a href="#" id="oauth">here</a> to find out your OAuth token</p>
<label for="token">OAuth Token</label><input type="text" name="token" id="token" value="{{token}}"> <br>
</fieldset>
<fieldset>
<legend>Directories</legend>
<label for="blackhole_dir">Blackhole Directory</label><input type="text" name="blackhole_dir" id="blackhole_dir" value="{{blackhole_dir}}"> <br>
<label for="incomplete_dir">Incomplete Directory</label><input type="text" name="incomplete_dir" id="incomplete_dir" value="{{incomplete_dir}}"> <br>
<label for="download_dir">Download Directory</label><input type="text" name="download_dir" id="download_dir" value="{{download_dir}}"> <br>
</fieldset>
<fieldset>
<legend>Intervals</legend>
<label for="polling_interval">Poll for completed transfers (minutes)</label><input type="text" name="polling_interval" id="polling_interval" value="{{polling_interval}}"> <br>
<label for="inactive_interval">Poll this often after all transfers have finished (minutes)</label><input type="text" name="inactive_interval" id="inactive_interval" value="{{inactive_interval}}"> <br>
</fieldset>
<button class="smooth btn-b">Save</button>
</form>
<script>
$(document).ready(function () {
  $("a#oauth").click(function() {
    var id = $("#client_id").val();
    var secret = $("#client_secret").val();
    var url = ("https://api.put.io/v2/oauth2/authenticate?client_id="
              + id + "&response_type=token&redirect_uri=" + encodeURIComponent("http://anonfunc.github.io/holeio/token.html"));
    open(url);
  });
});
</script>
