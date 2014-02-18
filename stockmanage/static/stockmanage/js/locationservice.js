$(function () {
            var serviceUrl_addmodify = "/stockmanage/location_add_modify/";
            var serviceUrl_delete = "/stockmanage/location_delete/";
            var serviceUrl_get="/stockmanage/location_get/";
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
                                    $.post(serviceUrl_addmodify,
                                                {"csrfmiddlewaretoken":csrf, "id": id, "parentId": parentId, "name": name, "code": code, "desc": desc }
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
                                    $.get(serviceUrl_delete+id
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
                $.get(serviceUrl_get+posId
                 , function (data) {
                 	 id=data[0].pk;
                 	 fields=data[0].fields;
                     $("#hiId").val(id);
                     $("#name").val(fields.Name);
                     $("#desc").val(fields.Description);
                     $("#code").val(fields.LocationCode);
                     $("#hiParentId").val(fields.ParentLocation);
                     $("#dvPositionForm").dialog("open");
                 }
            );

            });
        });