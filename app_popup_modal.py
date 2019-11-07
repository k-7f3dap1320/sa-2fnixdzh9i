""" Popup and modal messages """

def gen_tour_popup(tour, burl):
    """ Generate popup modal message after user is created (dashboard) """
    return_data = ''
    label_header = 'Welcome to SmartAlpha'
    label_content = 'Before you start, let us show you quickly some of the top features.'
    label_button = 'Take me to the quick tour'


    if tour == '1':
        return_data = '' +\
        '  <script type="text/javascript">'+\
        '  $(window).on(\'load\',function(){'+\
        '    $(\'#portf_popup\').modal(\'show\');'+\
        '  });'+\
        '  </script>'+\
        ' <div class="modal" id="portf_popup">'+\
        '    <div class="modal-dialog modal-lg">'+\
        '      <div class="modal-content">'+\
        '        <div class="modal-header">'+\
        '          <h4 class="modal-title">'+ label_header +'</h4>'+\
        '          <button type="button" class="close" data-dismiss="modal">&times;</button>'+\
        '        </div>'+\
        '        <div class="modal-body">'+\
        label_content +\
        '        </div>'+\
        '        <!-- Modal footer -->'+\
        '        <div class="modal-footer">'+\
        '          <button type="button" class="btn btn-info form-signin-btn" '+\
        'onClick="window.location.href=\''+ burl +'h\'">'+ label_button +'</button>'+\
        '        </div>'+\
        '      </div>'+\
        '    </div>'+\
        ' </div>'
    return return_data

def gen_portf_popup(pop):
    """ Generate popup modal after successfully create a strategy portfolio """
    return_data = ''
    label_header = 'Trading strategy created!'
    label_content = 'Your trading strategy has been generated.'
    label_button = 'Take me to my strategy...'

    if pop == '1':
        return_data = '' +\
        '  <script type="text/javascript">'+\
        '  $(window).on(\'load\',function(){'+\
        '    $(\'#portf_popup\').modal(\'show\');'+\
        '  });'+\
        '  </script>'+\
        ' <div class="modal" id="portf_popup">'+\
        '    <div class="modal-dialog modal-lg">'+\
        '      <div class="modal-content">'+\
        '        <div class="modal-header">'+\
        '          <h4 class="modal-title">'+ label_header +'</h4>'+\
        '          <button type="button" class="close" data-dismiss="modal">&times;</button>'+\
        '        </div>'+\
        '        <div class="modal-body">'+\
        label_content +\
        '        </div>'+\
        '        <!-- Modal footer -->'+\
        '        <div class="modal-footer">'+\
        '          <button type="button" class="btn btn-info form-signin-btn" '+\
        'data-dismiss="modal">'+ label_button +'</button>'+\
        '        </div>'+\
        '      </div>'+\
        '    </div>'+\
        ' </div>'
    return return_data

def get_portf_delete_data_toggle(uid):
    """ Add this function inside a button or a href """
    return_data = 'data-toggle="modal" data-target="#popup_delete_'+ str(uid) +'"'
    return return_data

def set_modal_delete_n_view_popup(portf_name, portf_id, burl, user_portf):
    """ popup message for delete confirmation from list of strategy portfolio """
    return_data = ''
    l_delete_message_caption = 'Are you sure you want to delete this strategy? ' +\
    '<br /><strong>'+ portf_name + '</strong>'
    l_cancel_button = 'Cancel'
    l_delete_button = 'Delete'
    delete_url_redirect_list = burl +'p/?delete='+ str(portf_id)
    delete_url_redirect_dash = burl +'p/?delete='+ str(portf_id) + '&dashboard=1'

    if user_portf:
        delete_url = delete_url_redirect_dash
    else:
        delete_url = delete_url_redirect_list

    l_view_message_caption = 'View or edit your strategy:' +\
    '<br /><strong>'+ portf_name + '</strong>'
    l_view_button = 'Take me to my trading strategy'

    return_data = '' +\
    '  <div class="modal" id="popup_delete_'+ str(portf_id) +'">'+\
    '    <div class="modal-dialog modal-dialog-centered">'+\
    '      <div class="modal-content">'+\
    '        <div class="modal-body">'+\
    l_delete_message_caption +\
    '        </div>'+\
    '        <div class="modal-footer">'+\
    '          <button type="button" class="btn btn-secondary" data-dismiss="modal">'+\
    l_cancel_button +'</button>'+\
    '           <a class="btn btn-danger" href="'+ delete_url +'">'+ l_delete_button +'</a>'+\
    '        </div>'+\
    '       </div>'+\
    '     </div>'+\
    '   </div>'

    return_data = return_data  +\
    '  <div class="modal" id="popup_view_'+ str(portf_id) +'">'+\
    '    <div class="modal-dialog modal-dialog-centered">'+\
    '      <div class="modal-content">'+\
    '        <div class="modal-body">'+\
    l_view_message_caption +\
    '        </div>'+\
    '        <div class="modal-footer">'+\
    '          <button type="button" class="btn btn-secondary" data-dismiss="modal">'+\
    l_cancel_button +'</button>'+\
    '           <a class="btn btn-info" href="'+ burl +'p/?uid='+ str(portf_id) +'">'+\
    l_view_button +'</a>'+\
    '        </div>'+\
    '       </div>'+\
    '     </div>'+\
    '   </div>'
    return return_data
