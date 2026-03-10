(function(){
    const path = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    document.querySelectorAll(".navlinks a[data-page]").forEach(a => {
      const p = (a.getAttribute("data-page") || "").toLowerCase();
      if (p === path) a.classList.add("active");
    });
  })();
  