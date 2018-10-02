///////////////// Get the list of routers for the selected Network //////////////////////////////////////////////////

$('#network').on('change', () => {
  var asn = $("select[name=network").val()
  $.ajax({
    url: `/routers/${asn}`,
    type: 'get',
    success: function (data) {
      updateRouters(JSON.parse(data));
    },
    error: function (err) {
      console.log(err)
    }
  })
})

function updateRouters (routers) {
  console.log(routers)
  $('#router').empty();
  $('#router').prop('disabled', false);
  $('#router').append($('<option>', {
    value: "",
    text: "",
    disabled: true,
    selected: true
  }))
  routers.forEach(function (r) {
    $('#router').append($('<option>', {
      value: r.name,
      text: r.location,
      type: r.type
    }))
  })
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////// Submit Form  //////////////////////////////////////////////////////////////////////////////

$('#lgForm').on('submit', function () {submitForm()})

var submitForm = function() {

  $('#loading').show();
  var cmd = $('input[name=cmd]:checked', '#lgForm').val();
  var router = $('#router option:selected').val();
  var ipprefix = $('#ipprefix').val();
  var routerType = $('#router option:selected').attr('type')

  var command = getCommandSyntax(cmd, routerType, ipprefix);

  $('#results').text("")
  $('#queryInfo').text("")

  $('#queryInfo').html(`
<b>Network: </b> ${$("#network option:selected").text()}
<b>Router: </b> ${router}
<b>Command: </b> ${command}`)

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/lg', true);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8')
  xhr.send(JSON.stringify({router: router, cmd: cmd, ipprefix: ipprefix}));

  xhr_timer = window.setInterval(function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      $('#loading').hide();
      window.clearTimeout(xhr_timer);
    }
    document.getElementById('results').innerHTML = xhr.responseText;
  }, 500);

  xhr.addEventListener("error", function(e) {
    console.log("error: " + e);
  });

}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////

function getCommandSyntax(cmd, routerType, ipprefix) {

  switch (cmd) {
    case 'bgp':
      switch (routerType) {
        case 'JunOS':
          return `show route protocol bgp ${ipprefix} table inet.0 detail`
        case 'IOS-XR':
          return `show bgp ipv4 unicast ${ipprefix}`
      }
    case 'ping':
      return `ping ${ipprefix} count 5`
    case 'traceroute':
      switch (routerType) {
        case 'JunOS':
          return `traceroute ${ipprefix} wait 2`
        case 'IOS-XR':
          return `traceroute ${ipprefix} timeout 2 probe 2`
      }
  }
}