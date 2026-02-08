const course = { creator_id: 2 };
const user = { id: 1, role: 'superadmin' };

const isOwner = parseInt(course.creator_id) === parseInt(user.id);
const isAdmin = user.role === 'admin';
const isSuperAdmin = user.role === 'superadmin';

console.log('User ID:', user.id);
console.log('Course Creator ID:', course.creator_id);
console.log('User Role:', user.role);
console.log('Is Owner?', isOwner);
console.log('Is Admin?', isAdmin);
console.log('Is SuperAdmin?', isSuperAdmin);

if (!isOwner && !isSuperAdmin && !isAdmin) {
    console.log('Outcome: 403 Forbidden');
} else {
    console.log('Outcome: 200 OK (Allowed)');
}
