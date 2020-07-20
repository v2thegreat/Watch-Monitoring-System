package com.example.systemmonitoring;

import android.os.Bundle;
import android.support.wearable.activity.WearableActivity;
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

import java.util.Calendar;

public class MainActivity extends WearableActivity {

    private ProgressBar progressBarCPU, progressBarMemory;
    private TextView txtViewDiskRead, txtViewDiskWrite, txtviewLastRefreshed;
    private int i = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button refreshButton = findViewById(R.id.toastButton);
        progressBarCPU = findViewById(R.id.progressBarCPU);
        progressBarMemory = findViewById(R.id.progressBarMemory);
        txtViewDiskRead = findViewById(R.id.txtViewDiskRead);
        txtViewDiskWrite = findViewById(R.id.txtViewDiskWrite);
        txtviewLastRefreshed = findViewById(R.id.txtviewLastRefreshed);

        getServerInformation();
        refreshButton.setOnClickListener(new View.OnClickListener() {
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

                    String disk_read = jsonObject.getString("diskRead");
                    String disk_write = jsonObject.getString("diskWrite");
                    String new_read_string = getResources().getString(R.string.disk_read_title).replace("{}", disk_read);
                    String new_write_string = getResources().getString(R.string.disk_write_title).replace("{}", disk_write);

                    progressBarCPU.setProgress(cpu_usage_percentage, true);
                    progressBarMemory.setProgress(memory_usage_percentage, true);
                    txtViewDiskRead.setText(new_read_string);
                    txtViewDiskWrite.setText(new_write_string);

                    txtviewLastRefreshed.setText(Calendar.getInstance().getTime().toString());
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
