$(function () {
            //$("#billeditor").tabs();
            $("#btn_save").click(function(){
            	$("#fm_detail_update").submit();
            });
            $('#btn_apply').confirmation();
        });