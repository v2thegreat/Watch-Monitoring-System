package com.example.systemmonitoring;

import android.os.Bundle;
import android.support.wearable.activity.WearableActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends WearableActivity {

    private TextView serverCount;
    private Button toastButton;
    private ProgressBar progressBarCPU, progressBarMemory;
    private RequestQueue requestQueue;
    private int i = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        serverCount = findViewById(R.id.SystemInformation);
        toastButton = findViewById(R.id.toastButton);
        progressBarCPU = findViewById(R.id.progressBarCPU);
        progressBarMemory = findViewById(R.id.progressBarMemory);

        getServerInformation();
        toastButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                getServerInformation();
            }
        });
        // Enables Always-on
        setAmbientEnabled();
    }

    private void getServerInformation() {
// ...

// Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);
        String url = "http://192.168.1.11:5590/minimal";

        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                try {
                    JSONObject jsonObject = new JSONObject(response);
                    int cpu_usage_percentage = jsonObject.getInt("cpu");
                    int memory_usage_percentage = jsonObject.getInt("memory");
                    progressBarCPU.setProgress(cpu_usage_percentage);
                    progressBarMemory.setProgress(memory_usage_percentage);
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                error.printStackTrace();
                Toast.makeText(getApplicationContext(), "Error Raised!", Toast.LENGTH_SHORT).show();
            }
        });

        stringRequest.setRetryPolicy(new DefaultRetryPolicy(
                5000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
        );
        queue.add(stringRequest);
    }
}
