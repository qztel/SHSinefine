$(document).ready(function() {
  $('#select-site').select2()
  $('#select-site-table').css('display', 'none')

  let type_id = false
  let site_id = false

  $(".o_delivery_carrier_select").click(function() {
    let way = $(this).children('label').text()
    type_id = $(this).children('input').val()

    delivery_type_select_ajax(type_id, site_id)

    if (way == '站点自提'){
      $('#select-site-table').css('display', 'block')
    } else {
      $('#select-site-table').css('display', 'none')
      $('#select-site').val('0')
      $('.select2-selection__rendered').text('请选择')
    }
  })

  $('#select-site').change(function() {
    site_id = $(this).val()
  })


  function delivery_type_select_ajax(type_id, val_id) {
    url = '/select/delivery/type'
    let data = {
      type_id: type_id,
      site_id: site_id,
    }
    $.post(url,data,function(result){
       console.log(result)
    })
  }
})
