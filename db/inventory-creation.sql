/**
*
*/
CREATE TABLE company (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(120) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    company_id BIGINT,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('superadmin', 'admin', 'employee')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_users_role_company
        CHECK (
            (role = 'superadmin' AND company_id IS NULL) OR
            (role IN ('admin', 'employee') AND company_id IS NOT NULL)
        ),
    CONSTRAINT fk_users_company
        FOREIGN KEY (company_id) REFERENCES company(id)
        ON DELETE SET NULL
);


CREATE TABLE providers (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    tel VARCHAR(30),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    image_url TEXT,
    name VARCHAR(120) NOT NULL,
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    provider_id BIGINT,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_items_provider
        FOREIGN KEY (provider_id) REFERENCES providers(id)
        ON DELETE SET NULL
);

CREATE TABLE inventory_movements (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    item_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    movement_type VARCHAR(20) NOT NULL CHECK (
        movement_type IN ('add', 'sale', 'dispatch', 'adjustment')
    ),
    quantity INT NOT NULL CHECK (quantity > 0),
    note TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_movements_item
        FOREIGN KEY (item_id) REFERENCES items(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_movements_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);
