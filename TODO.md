# TODO - Student Course Enrollment & Certificate Flow

## ✅ Phase 1: Profile Completion Alert - COMPLETED
- [x] 1.1 Add profile completion check in student dashboard view
- [x] 1.2 Update student dashboard template to show alert if profile incomplete
- [x] 1.3 Create profile edit form and view (student_profile_update)

## ✅ Phase 2: Show Institutes & Courses - COMPLETED
- [x] 2.1 Update student dashboard view to fetch approved institutes and courses
- [x] 2.2 Update student dashboard template to display institutes/courses

## ✅ Phase 3: Course Enrollment Request - COMPLETED
- [x] 3.1 Create enrollment request view (enroll_course)
- [x] 3.2 Add URL for enrollment
- [x] 3.3 Student can select institute & course to enroll

## ✅ Phase 4: Institute Approval Workflow - COMPLETED
- [x] 4.1 Add view for institute to see pending enrollments (manage_enrollments)
- [x] 4.2 Add approve/reject functionality (update_enrollment)
- [x] 4.3 Update institute dashboard with link to manage enrollments

## ✅ Phase 5: Course Completion - COMPLETED
- [x] 5.1 Add view for institute to mark course as completed (update_enrollment with 'complete' action)

## ⏳ Phase 6: Certificate Request (To be implemented)
- [ ] 6.1 Allow student to request certificate after completion
- [ ] 6.2 Institute can issue certificate

## Files Modified/Created:
- accounts/views.py - Added student_dashboard, student_profile_update, enroll_course
- accounts/urls.py - Added new URLs
- students/models.py - Already has Enrollment model
- institute/views.py - Added manage_enrollments, update_enrollment
- institute/urls.py - Added new URLs
- templates/student/dashboard.html - Updated with new UI
- templates/student/profile_update.html - Created
- templates/institute/manage_enrollments.html - Created
- templates/institute/institution_dashboard.html - Updated sidebar

