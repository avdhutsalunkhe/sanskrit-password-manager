document.addEventListener("DOMContentLoaded", () => {
	gsap.from(".container", {
	  opacity: 0,
	  scale: 0.9,
	  duration: 1,
	  ease: "back.out(1.7)",
	});
  
	gsap.from(".student-form input, .student-form button", {
	  y: 30,
	  opacity: 0,
	  duration: 0.8,
	  stagger: 0.1,
	  ease: "power2.out",
	});
  
	gsap.from(".student-table tbody tr", {
	  x: -50,
	  opacity: 0,
	  duration: 1,
	  stagger: 0.2,
	  ease: "power2.out"
	});
  });
  