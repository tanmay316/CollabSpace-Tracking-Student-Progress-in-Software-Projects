<template>
    <div class="mc">
        <div class="mentorship-session">
            <img src="https://via.placeholder.com/100" alt="Mentor Image" class="mentor-image" />
            <div class="session-details">
            <h3 class="session-title">Mentorship Session Title</h3>
            <p class="mentor-name">Anurag</p>
            <p class="session-description">
                This is a detailed description of the mentorship session, covering the topics that will be addressed.
            </p>
            <p class="session-amount">$150</p>
            </div>
        </div>
        <div class="mentorship-session">
            <img src="https://via.placeholder.com/100" alt="Mentor Image" class="mentor-image" />
            <div class="session-details">
            <h3 class="session-title">Mentorship Session Title</h3>
            <p class="mentor-name">Anurag</p>
            <p class="session-description">
                This is a detailed description of the mentorship session, covering the topics that will be addressed.
            </p>
            <p class="session-amount">$150</p>
            </div>
        </div>
    </div>
</template>
  
<style scoped>
.mc{
    margin-top: 5rem;
    display: flex;
    flex-direction: column;
}

.mentorship-session {
display: flex;
align-items: flex-start;
background-color: #fff;
padding: 16px;
border-radius: 8px;
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
margin-bottom: 16px;
}

.mentor-image {
width: 100px;
height: 100px;
object-fit: cover;
border-radius: 8px;
margin-right: 16px;
}

.session-details {
flex: 1;
}

.session-title {
color: #717171;
font-size: 1.25rem;
font-weight: bold;
margin-bottom: 8px;
}

.mentor-name {
font-size: 1rem;
font-weight: 600;
margin-bottom: 8px;
color: #1f2937; /* Dark text */
}

.session-description {
font-size: 0.9rem;
color: #4b5563; /* Medium text */
margin-bottom: 12px;
}

.session-amount {
font-size: 1.1rem;
font-weight: bold;
color: #10b981; /* Green text */
}
</style>
