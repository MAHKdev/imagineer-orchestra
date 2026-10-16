// Orchestra Settings -- "Test Connection" button
// Checks that the Orchestra server is reachable by fetching /concerto/bridge.js.
frappe.ui.form.on("Orchestra Settings", {
  refresh: function (frm) {
    frm.add_custom_button("Test Connection", function () {
      var url = (frm.doc.orchestra_url || "").replace(/\/$/, "");
      if (!url) {
        frappe.msgprint("Enter an Orchestra URL first");
        return;
      }
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
