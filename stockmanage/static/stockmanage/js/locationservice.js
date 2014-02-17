$(function () {
            var serviceUrl = "/stockmanage/locationmanage/";
            var diag = $("#dvPositionForm").dialog({
                width: 370,
                autoOpen: false,
                buttons: [
                            {
                                text: "保存",
                                click: function () {
                                    var id = $("#hiId").val();
                                    var parentId = $("#hiParentId").val();
                                    var name = $("#name").val();
                                    var desc = $("#desc").val();
                                    var code = $("#code").val();
                                    var csrf=$.cookie("csrftoken");
                                    $.post(serviceUrl,
                                                {"csrfmiddlewaretoken":csrf, "actiontype": "position_addmodify", "id": id, "parentId": parentId, "name": name, "code": code, "desc": desc }
                                                , function (returnId) {
                                                    $("#hiId").val(returnId);
                                                    $("#spMsg").show();
                                                    $("#spMsg").fadeOut(3000);
                                                    window.location = window.location;
                                                }
                                                );
                                }
                            }
                    ,
                            {
                                text: "关闭",
                                click: function () {
                                    $(this).dialog("close");
                                }
                            }
                    ,
                            {
                                id: "dialog_button_delete",
                                text: "删除",
                                click: function () {
                                    var name = $("#name").val();
                                    var id = $("#hiId").val();
                                    if (!confirm("确定要删除:  \"" + name + "\" 么?")) return false;
                                    $.get(serviceUrl, { actiontype: "position_delete", id: id }
                                        , function (data) {
                                            if (data != "")
                                            { alert(data); }
                                            else {
                                                $("[posid=" + id + "]").parent().remove();
                                            }
                                           
                                                     }
                                        );
                                        $(this).dialog("close");
                                }
                            }
                ]
            });
            $(".dvAdd")
              .click(function () {
                  $("#dialog_button_delete").hide();
                  $("#hiId").val("");
                  $("#name").val("");
                  $("#desc").val("");
                  $("#code").val("");
                  var parentId = $(this).siblings(".posName").attr("posId");
                  $("#hiParentId").val(parentId);
                 diag= $("#dvPositionForm").dialog("open");
              });
            //修改
            $(".posName").click(function () {
                $("#dialog_button_delete").show();
                var posId = $(this).attr("posId");
                $.get(serviceUrl,
                 { "actiontype": "position_get", "id": posId }
                 , function (data) {
                     $("#hiId").val(data.id);
                     $("#name").val(data.name);
                     $("#desc").val(data.desc);
                     $("#code").val(data.code);
                     $("#dvPositionForm").dialog("open");
                 }
            );

            });
        });