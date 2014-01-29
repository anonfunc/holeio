%rebase base
<!DOCTYPE html>
<h1>Hole.io Config</h1>
<form action="config" method="post">
<fieldset>
<legend>Web Configuration</legend>
<label for="Host">Host</label><input type="text" name="host" id="host" value="{{host}}"> <br>
</fieldset>
<fieldset>
<legend>OAuth Configuration</legend>
<label for="client_id">Client ID</label><input type="text" name="client_id" id="client_id" value="{{client_id}}"> <br>
<label for="client_secret">Client Secret</label><input type="text" name="client_secret" id="client_secret" value="{{client_secret}}"> <br>
</fieldset>
<fieldset>
<legend>Directories</legend>
<label for="blackhole_dir">Blackhole Directory</label><input type="text" name="blackhole_dir" id="blackhole_dir" value="{{blackhole_dir}}"> <br>
<label for="download_dir">Download Directory</label><input type="text" name="download_dir" id="download_dir" value="{{download_dir}}"> <br>
</fieldset>
<button class="smooth btn-b">Save</button>
</form>
