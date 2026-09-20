function save() {
  localStorage.setItem(
    "theme",
    document.body.classList.contains("light") ? "light" : "dark",
  );
}
const thmBtn = document.getElementById("themeBtn");
thmBtn.addEventListener("click", () => {
  document.body.classList.toggle("light");
  save();
});
const savedTheme = localStorage.getItem("theme");
function loadTheme() {
  if (savedTheme === "light") {
    document.body.classList.add("light");
  } else {
    document.body.classList.remove("light");
  }
}

loadTheme();

const navButtons = document.querySelectorAll(".navBtn");
const sections = document.querySelectorAll(
  "#overview-section, #features-section, #translator-section, #roles-section, #admins, #HOO, #socials-section, #join-section",
);

navButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    const targetId = btn.dataset.target;
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: "smooth" });
    }
  });
});

function setActiveNav(targetId) {
  navButtons.forEach((btn) => {
    if (btn.dataset.target === targetId) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

const observerOptions = {
  root: null,
  rootMargin: "-25% 0px -45% 0px",
  threshold: 0,
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting && window.scrollY >= window.innerHeight * 0.15) {
      setActiveNav(entry.target.id);
    }
  });
}, observerOptions);

sections.forEach((section) => observer.observe(section));

window.addEventListener("scroll", () => {
  if (window.scrollY < window.innerHeight * 0.15) {
    setActiveNav("overview-section");
  }
});

const joinBtn = document.querySelector(".joinBtn");
if (joinBtn) {
  joinBtn.addEventListener("click", () => {
    window.location.href = "https://discord.gg/E2PRC2csAx";
  });
}

// --- Translator Logic ---
const translateBtn = document.getElementById("translateBtn");
const darijaInput = document.getElementById("darijaInput");
const englishOutput = document.getElementById("englishOutput");

async function handleTranslation() {
  const text = darijaInput.value.trim();
  if (!text) return;

  englishOutput.value = "Translating...";

  try {
    const response = await fetch("/api/index", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });

    const data = await response.json();
    if (data.translation) {
      englishOutput.value = data.translation;
    } else {
      englishOutput.value = "Error: " + (data.error || "Failed to translate");
    }
  } catch (err) {
    englishOutput.value = "Error connecting to translation server.";
  }

  darijaInput.value = "";
}

translateBtn.addEventListener("click", handleTranslation);

darijaInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    handleTranslation();
  }
});
