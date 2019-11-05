# Copyright (c) 2018-present, Taatu Ltd.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

def gen_portf_popup(uid,pop):
    r = ''
    try:
        label_header = 'Trading strategy created!'
        label_content = ''
        label_button = 'Take me to my strategy...'

        if pop == '1':
            r = '' +\
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
            '          <button type="button" class="btn btn-info form-signin-btn" data-dismiss="modal">'+ label_button +'</button>'+\
            '        </div>'+\
            '      </div>'+\
            '    </div>'+\
            ' </div>'

    except Exception as e: print(e)
    return r
