const form = document.querySelector('#search-form');
const button = document.querySelector('#search');
const status = document.querySelector('#status');
const weather = document.querySelector('#weather');
const iconMap = { '01':'☀', '02':'⛅', '03':'☁', '04':'☁', '09':'☂', '10':'☂', '11':'⚡', '13':'❄', '50':'≋' };
const set = (id, value) => document.querySelector(`#${id}`).textContent = value;

form.addEventListener('submit', async (event) => {
	event.preventDefault();
	button.disabled = true; status.textContent = 'Reading the latest conditions...'; weather.classList.remove('visible');
	try {
		const response = await fetch(`/api/weather?city=${encodeURIComponent(document.querySelector('#city').value.trim())}`);
		const data = await response.json();
		if (!response.ok) throw new Error(data.detail || 'Could not load weather.');
		set('place', `${data.city}, ${data.country}`); set('date', new Date().toLocaleDateString(undefined, {weekday:'long', month:'long', day:'numeric'}));
		set('icon', iconMap[data.icon.slice(0,2)] || '◌'); set('temp', Math.round(data.temperature)); set('summary', data.description);
		set('feels', `${Math.round(data.feels_like)}°C`); set('humidity', `${data.humidity}%`); set('wind', `${data.wind_speed} m/s`); set('pressure', `${data.pressure} hPa`); set('visibility', `${data.visibility} km`); set('clouds', `${data.clouds}%`);
		weather.classList.add('visible'); status.textContent = '';
	} catch (error) { status.textContent = error.message; }
	finally { button.disabled = false; }
});
