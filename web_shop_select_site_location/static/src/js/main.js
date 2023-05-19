$(document).ready(function() {
  $('#select-site').select2()
  $('#select-site-table').css('display', 'none')

  $(".o_delivery_carrier_select").click(function() {
    const way = $(this).children('label').text()
    const self = $(this)

//    delivery_type_select_ajax(self)

    if (way == '站点自提'){
      $('#select-site-table').css('display', 'block')
    } else {
      $('#select-site-table').css('display', 'none')
      $('#select-site-table').val('0')
    }
  })


  function delivery_type_select_ajax(self, val_id) {
    const type_id = self.children('input').val()
    const site_id = $('#select-site').val()

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