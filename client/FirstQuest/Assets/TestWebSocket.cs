using System;
using UnityEngine;
using WebSocketSharp;

[Serializable]
public class TestMessage
{
    public string user_id;
    public string password;
}

public class TestWebSocket : MonoBehaviour {

    WebSocket ws;

    // Use this for initialization
    void Start () {
        ws = new WebSocket("ws://gkf.iobb.net:8000/login");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket Open");
        };

        ws.OnMessage += (sender, e) =>
        {
            Debug.Log("WebSocket Message Type: " + e.GetType() + ", Data: " + e.Data);
        };

        ws.OnError += (sender, e) =>
        {
            Debug.Log("WebSocket Error Message: " + e.Message);
        };

        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket Close");
        };

        ws.Connect();
    }
	
	// Update is called once per frame
	void Update () {
        if (Input.GetKeyUp("s"))
        {
            TestMessage obj = new TestMessage();
            obj.user_id = "test";
            obj.password = "hoge";
            ws.Send(JsonUtility.ToJson(obj));
        }
        if (Input.GetKeyUp("a"))
        {
            TestMessage obj = new TestMessage();
            obj.user_id = "test";
            obj.password = "password";
            ws.Send(JsonUtility.ToJson(obj));
        }

    }

    void OnDestroy()
    {
        ws.Close();
        ws = null;
    }
}
