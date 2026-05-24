Inventory management system API documentatio

This APi is the core of the inventory management system, providing endpoints for managing products, categories, and inventory levels. It allows users to perform CRUD operations on products and categories, as well as track inventory levels and generate reports.

The project has users  admin, user and root

Admin: Admin users have full access to all endpoints and can perform any action, including creating, updating, and deleting on all endpoints

Theres gonna be a organization tab where admin users can manage their organization details, including adding and removing users, setting permissions

Users can update the inventory, view reports, and manage their own profile. They can also view the products and categories but cannot create,, or delete them.

CRUD for organizations 
Access: Root only

CRUD for users
Access: Admin and Root

CRUD for products
Access: Admin and Root
READ users can view products but cannot create, delete, they will be able to update certain product features and details

CRUD for categories
Access: Admin and Root
READ users can view categories but cannot create, delete, they will be able to update certain category features and details

LOGS Access: Admin and Root
Admin and Root users can access logs to monitor system activity, track changes, and identify any issues

CRUD items
Access: Admin and Root, and users on certain features

Providers can manage their inventory levels, update product details, and view reports related to their products. They can also access logs to monitor their activity and track changes.