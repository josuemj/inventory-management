CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE organizations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        VARCHAR(120) NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id           UUID,
    supabase_user_id UUID UNIQUE,
    full_name        VARCHAR(100) NOT NULL,
    username         VARCHAR(50) NOT NULL UNIQUE,
    hashed_password  TEXT,
    role             VARCHAR(20) NOT NULL CHECK (role IN ('root', 'admin', 'member')),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_users_role_org
        CHECK (
            (role = 'root' AND org_id IS NULL) OR
            (role IN ('admin', 'member') AND org_id IS NOT NULL)
        ),
    CONSTRAINT fk_users_org
        FOREIGN KEY (org_id) REFERENCES organizations(id)
        ON DELETE SET NULL
);

CREATE TABLE categories (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id     UUID NOT NULL,
    name       VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_categories_org
        FOREIGN KEY (org_id) REFERENCES organizations(id)
        ON DELETE CASCADE
);

CREATE TABLE providers (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name       VARCHAR(100) NOT NULL,
    tel        VARCHAR(30),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE items (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id      UUID NOT NULL,
    category_id UUID,
    provider_id UUID,
    image_url   TEXT,
    name        VARCHAR(120) NOT NULL,
    price       DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    stock       INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_items_org
        FOREIGN KEY (org_id) REFERENCES organizations(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_items_category
        FOREIGN KEY (category_id) REFERENCES categories(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_items_provider
        FOREIGN KEY (provider_id) REFERENCES providers(id)
        ON DELETE SET NULL
);

CREATE TABLE inventory_movements (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    item_id       UUID NOT NULL,
    user_id       UUID NOT NULL,
    movement_type VARCHAR(20) NOT NULL CHECK (
        movement_type IN ('add', 'sale', 'dispatch', 'adjustment')
    ),
    quantity      INT NOT NULL CHECK (quantity > 0),
    note          TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_movements_item
        FOREIGN KEY (item_id) REFERENCES items(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_movements_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE change_logs (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id      UUID NOT NULL,
    user_id     UUID NOT NULL,
    entity_type VARCHAR(50) NOT NULL CHECK (
        entity_type IN ('item', 'category', 'user', 'organization')
    ),
    entity_id   UUID NOT NULL,
    field       VARCHAR(100) NOT NULL,
    old_value   TEXT,
    new_value   TEXT,
    changed_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT fk_logs_org
        FOREIGN KEY (org_id) REFERENCES organizations(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_logs_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);
