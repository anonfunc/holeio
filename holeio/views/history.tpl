  %rebase base
  <h1>History</h1>
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
