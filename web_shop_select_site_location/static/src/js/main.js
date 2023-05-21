$(document).ready(function() {
  $('#select-site').select2()
  $('#select-site-table').css('display', 'none')

  let type_id = ''
  let site_id = ''
  let csrf_token = $("input[name='csrf_token']").val()

  $(".o_delivery_carrier_select").click(function() {
    let way = $(this).children('label').text()
    type_id = $(this).children('input').val()

    delivery_type_select_ajax(type_id, site_id, csrf_token)

    if (way == '站点自提'){
      $('#select-site-table').css('display', 'block')
    } else {
      $('#select-site-table').css('display', 'none')
      $('#select-site').val('0')
      $('.select2-selection__rendered').text('请选择')
      console.log($('#select-site').val())
    }
  })

  $('#select-site').change(function() {
    site_id = $(this).val()
    delivery_type_select_ajax(type_id, site_id, csrf_token)
  })


  function delivery_type_select_ajax(type_id, val_id) {
    url = '/select/delivery/type'
    let data = {
      type_id: type_id,
      site_id: site_id,
      csrf_token: csrf_token
    }
    $.post(url,data,function(result){
       console.log(result)
    })
  }
})