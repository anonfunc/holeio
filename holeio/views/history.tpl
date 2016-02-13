  %rebase base
  <div class="row">
    <column class="c4">
      <a href="wake">Check for Finished Downloads</a>
    </column>
    <column class="c6">
      <form action="magnet" method="post">
        <span class="addon-front">+</span><input class="smooth" type="text" name="uri" id="uri" placeholder="Magnet URI"> <br>
      </form>
    </column>
  </div>
  <hr>
  <h3>History <a href="clearhistory">Clear</a></h3>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Time</th>
        <th>Message</th>
      </tr>
    </thead>
    % for row in history:
    <tr>
      <td>{{row[0]}}</td>
      <td>{{row[1]}}</td>
    </tr>
    % end
  </table>
