<%@ Page Title="" Language="C#" MasterPageFile="~/site_showroom.master" AutoEventWireup="true"
    CodeFile="PositionManage.aspx.cs" Inherits="Admin_Showroom_PositionManage" %>

<asp:Content ID="Content1" ContentPlaceHolderID="head" runat="Server">
   
    <link href="/Admin/css/showroommanage.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript">
        $(function () {
            var serviceUrl = "/services/showroomservice.ashx";
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
                                    $.post(serviceUrl,
                                                { "actiontype": "position_addmodify", "id": id, "parentId": parentId, "name": name, "code": code, "desc": desc }
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
                $.get("/services/showroomservice.ashx",
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
    </script>
</asp:Content>

<asp:Content ID="Content3" ContentPlaceHolderID="cph_maincontent" runat="Server">
    <asp:Repeater runat="server" ID="rpLv1">
        <HeaderTemplate>
        </HeaderTemplate>
        <ItemTemplate>
           <div class="dvContainerLv1">
                <h2 class="posName" posid='<%#Eval("id") %>'>
                    <%#Eval("Name") %></h2>
                    <asp:Repeater runat="server" ID="rpgLv2">
                        <HeaderTemplate>
                        </HeaderTemplate>
                        <ItemTemplate>
                          <div class="dvContainerLv2">
                                 <h3 class="posName" posid='<%#Eval("id")%>'>
                                    <%#Eval("Name") %></h3>
                             
                                    <asp:Repeater runat="server" ID="rpgLv3">
                                    <HeaderTemplate> 
                                    </HeaderTemplate>
                                        <ItemTemplate>
                                             <div class="dvContainerLv3"">
                                               <span class="posName" posid='<%#Eval("id") %>'><%#Eval("Name") %></span> 
                                            </div>
                                        </ItemTemplate>
                                        <FooterTemplate>
                                            
                                        </FooterTemplate>
                                    </asp:Repeater>
                                     <div class="dvAdd">
                                                <span>增加展区</span></div>
                               
                            </div>
                        </ItemTemplate>
                        <FooterTemplate>
                           
                        
                        </FooterTemplate>
                    </asp:Repeater>
                 <div class="dvAdd">
                  <span >增加展厅</span></div>
            </div>
        </ItemTemplate>
        <FooterTemplate>
           
        </FooterTemplate>
            
    </asp:Repeater> 
    <div class="dvAdd">
      
      <span>增加展馆</span></div>
    <div id="dvPositionForm">
     <input type="hidden" id="hiId" />
     <input type="hidden" id="hiParentId" />
         <fieldset>
            <label for="name">
                名称</label>
           
            <input type="text" name="name" id="name" class="text ui-widget-content ui-corner-all" />
            <label for="code">
                位置代码</label>
            <input type="text" name="code" id="code" value="" class="text ui-widget-content ui-corner-all" />
            <label for="description">
                位置描述</label>
            <input name="description" id="desc" value="" class="text ui-widget-content ui-corner-all" />
           <span id="spMsg"  class="hide success">保存成功</span>
        </fieldset>
    </div>
</asp:Content>
