// Orchestra Settings -- "Test Connection" button
// Checks that the Orchestra server is reachable by fetching /concerto/bridge.js.
frappe.ui.form.on("Orchestra Settings", {
  refresh: function (frm) {
    frm.add_custom_button("Test Connection", function () {
      // orchestra_url is a hidden debug field — empty means the hosted
      // default, so test that.
      var url = (frm.doc.orchestra_url || "https://orchestra.imagineer.solutions").replace(/\/$/, "");
      fetch(url + "/concerto/bridge.js")
        .then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          frappe.msgprint({
            title: "Connection Successful",
            message: "Orchestra server reachable at " + url,
            indicator: "green",
          });
        })
        .catch(function (err) {
          frappe.msgprint({
            title: "Connection Failed",
            message: "Could not reach Orchestra server: " + err,
            indicator: "red",
          });
        });
    });
  },
});
