<%@ WebHandler Language="C#" Class="ShowRoomService" %>

using System;
using System.Web;
using NBiz;
using NModel;
public class ShowRoomService : IHttpHandler {

    BizPosition bizPos = new BizPosition();
    public void ProcessRequest (HttpContext context) {

        string actionType = context.Request["actiontype"];
        string id = context.Request["id"];
        switch (actionType.ToLower())
        {
            
            case "position_addmodify":

                string parentId = context.Request["parentId"]; 
                string name = context.Request["name"];
                string code = context.Request["code"];
                string desc = context.Request["desc"];
                
              SR_Position posR=  SaveUpdatePosition(id,parentId, name, code, desc);
                context.Response.Write(posR.Id);
                break;
            case "position_get":
              SR_Position pos=  bizPos.GetOne(new Guid(id));
              string jsonPos = string.Format("{{\"id\":\"{0}\",\"name\":\"{1}\",\"code\":\"{2}\",\"desc\":\"{3}\" }}", pos.Id, pos.Name, pos.PositionCode, pos.Description);
              context.Response.ContentType = "application/json";
              context.Response.Write(jsonPos);
                break;
            case "position_delete":

                SR_Position posToDelete=bizPos.GetOne(new Guid(id));
                if(posToDelete.ChildrenPosition.Count>0)
                {
                context.Response.Write("删除失败.请先删除子项.");
                }
                else
                {
                bizPos.Delete(posToDelete);
                }
                break;
                
        }
    }
    
    public SR_Position SaveUpdatePosition(string id,string parentId,string name,string code,string desc)
    {
        SR_Position pos = null;
        if (!string.IsNullOrEmpty(id))
        {

             pos = bizPos.GetOne(new Guid(id));
        }
        if (pos==null)
        { pos = new SR_Position(); }

        SR_Position posParent = null;
        if (!string.IsNullOrEmpty(parentId))
        {

            posParent = bizPos.GetOne(new Guid(parentId));
        }
        
        pos.Description = desc;
        pos.Name = name;
        pos.PositionCode = code;
        
        if (posParent != null)
        {
            pos.ParentPosition = posParent;
            posParent.ChildrenPosition.Add(pos);
        
        }
        
        bizPos.SaveOrUpdate(pos);
        return pos;
    }
    public bool IsReusable {
        get {
            return false;
        }
    }

}